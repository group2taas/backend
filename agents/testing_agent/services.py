import tempfile
import asyncio
import os
import json
from loguru import logger
from agents.base.model_handler import AIModelHandler
from .prompts import TEST_CASE_GENERATION_PROMPT
from tickets.models import Ticket
from results.models import Result
from channels.layers import get_channel_layer

class TestingAgent:
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        self.ticket_obj = Ticket.objects.filter(id=ticket_id)
        self.result_obj, _ = Result.objects.get_or_create(ticket_id = ticket_id)
        self.group_name = f"test_status_{ticket_id}"

    async def process_output(self, line):
        cleaned_line = line.decode().strip()
        logger.info(f"Subprocess output: {cleaned_line}")
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            self.group_name,
            {
                "type": "test_status_update",
                "message": cleaned_line,
            }
        )

        try: 
            json_data = json.loads(cleaned_line)
            self.result_obj.add_log(json_data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON output: {cleaned_line}")
        
    
    async def read_output(self, stream, callback):
        while True:
            line = await stream.readline()
            if not line:
                break
            await self.process_output(line)


    def generate_test_cases_from_code(self, code):
        llm_model = AIModelHandler()
        
        prompt = TEST_CASE_GENERATION_PROMPT.format(testing_codebase = code)

        logger.info(f"Prompt sent to model to generate test cases: {prompt}")
        output = llm_model.query_model(prompt = prompt)
        print(output)
        return output


    def run_tests(self, code):
        
        test_cases = self.generate_test_cases_from_code(code)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        logger.info(f"Temporary test file created at: {tmp_file_path}")

        async def main_task():
            pass

        async def run_subprocess():
            sub_process = await asyncio.create_subprocess_exec(
                "python", "-u",  tmp_file_path, 
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )
            
            tasks = [
                asyncio.create_task(self.read_output(sub_process.stdout, print)),
                asyncio.create_task(self.read_output(sub_process.stderr, print)),
                asyncio.create_task(main_task())
            ]

            await asyncio.gather(*tasks)
            await sub_process.wait()

        try:
            asyncio.run(run_subprocess())
            self.ticket_obj.update(status="completed")
            logger.info(f"Ticket {self.ticket_id} marked as completed")
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
                logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
