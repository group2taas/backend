import tempfile
import asyncio
import os
import json
from loguru import logger
from agents.base.model_handler import AIModelHandler
from .prompts import TEST_CASE_GENERATION_PROMPT, PYTHON_SAMPLE_CODE
from tickets.models import Ticket
from results.models import Result
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer


class TestingAgent:
    def __init__(self, ticket_id, num_test_cases):
        self.ticket_id = ticket_id
        self.ticket_obj = Ticket.objects.filter(id=ticket_id)
        self.result_obj, _ = Result.objects.update_or_create(
            ticket_id=ticket_id, defaults={"num_tests": num_test_cases}
        )
        self.group_name = f"test_status_{ticket_id}"

    async def process_output(self, line):
        cleaned_line = line.decode().strip()
        logger.info(f"Subprocess output: {cleaned_line}")
        channel_layer = get_channel_layer()
        print(cleaned_line)
        await channel_layer.group_send(
            self.group_name,
            {
                "type": "test_status_update",
                "message": cleaned_line,
            },
        )

        try:
            json_data = json.loads(cleaned_line)
            await sync_to_async(self.result_obj.add_log)(json_data)
            if json_data.get("type") == "result":
                await sync_to_async(self.result_obj.update_test_results)(json_data)

                await channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "test_results_available",
                        "data": json_data,
                    },
                )

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON output: {cleaned_line}")
            await sync_to_async(self.result_obj.add_log)(
                {"type": "log", "message": cleaned_line}
            )

    async def read_output(self, stream, callback):
        while True:
            line = await stream.readline()
            if not line:
                break
            await self.process_output(line)

    def generate_test_cases_from_code(self, code):
        llm_model = AIModelHandler()

        prompt = TEST_CASE_GENERATION_PROMPT.format(testing_codebase=code)

        logger.info(f"Prompt sent to model to generate test cases: {prompt}")
        output = llm_model.query_model(prompt=prompt)
        print(output)
        return output

    def run_tests(self, code):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run_tests_async(code))
            loop.close()
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            self.ticket_obj.update(status="error")
            try:
                notif_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(notif_loop)
                notif_loop.run_until_complete(self._send_error_notification(str(e)))
                notif_loop.close()
            except Exception as notif_error:
                logger.error(f"Failed to send error notification: {notif_error}")

    async def _send_error_notification(self, error_message):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            self.group_name,
            {
                "type": "test_status_update",
                "message": json.dumps(
                    {
                        "type": "error",
                        "message": f"Failed to run security tests: {error_message}",
                    }
                ),
            },
        )

    async def run_tests_async(self, code):
        tmp_file_path = None
        try:
            test_cases = self.generate_test_cases_from_code(code)

            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                # tmp_file.write(code)
                tmp_file.write(PYTHON_SAMPLE_CODE)

                tmp_file_path = tmp_file.name

            logger.info(f"Temporary test file created at: {tmp_file_path}")

            async def monitor_process_health(process, timeout=900):
                try:
                    await asyncio.wait_for(process.wait(), timeout=timeout)
                    return process.returncode
                except asyncio.TimeoutError:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5)
                    except asyncio.TimeoutError:
                        process.kill()
                    return -1

            async def run_subprocess():

                sub_process = await asyncio.create_subprocess_exec(
                    "python",
                    "-u",
                    tmp_file_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                tasks = [
                    asyncio.create_task(self.read_output(sub_process.stdout, print)),
                    asyncio.create_task(self.read_output(sub_process.stderr, print)),
                    asyncio.create_task(monitor_process_health(sub_process)),
                ]

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Task exception: {result}")
                return results[-1]

            exit_code = await run_subprocess()

            if exit_code == 0:
                await sync_to_async(self.result_obj.save_overall_test_results)()
                await sync_to_async(self.ticket_obj.update)(status="completed")
                logger.info(f"Ticket {self.ticket_id} marked as completed")
            else:
                await sync_to_async(self.ticket_obj.update)(status="error")
                logger.error(f"Tests failed with exit code {exit_code}")

        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            await sync_to_async(self.ticket_obj.update)(status="error")

        finally:
            try:
                if tmp_file_path and os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                    logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
