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
from asgiref.sync import sync_to_async
from collections import defaultdict

class TestingAgent:
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        self.group_name = f"test_status_{ticket_id}"
        self.test_cases = defaultdict(set)

    async def process_output(self, line):
        cleaned_line = line.decode().strip()
        logger.info(f"Subprocess output: {cleaned_line}")
        try: 
            json_data = json.loads(cleaned_line)
            if not json_data.get("test_case") in self.test_cases:
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "test_status_update",
                        "message": cleaned_line,
                    }
                )
                self.test_cases[json_data.get("test_case")].add(cleaned_line)
                await sync_to_async(self.result_obj.add_log)(json_data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON output: {cleaned_line}")
            await sync_to_async (self.ticket_obj.update)(status = 'error')
        
    
    async def read_output(self, stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            await self.process_output(line)

        #for testing
        # for i in range(10):
        #     line = json.dumps({"test_case": f"test_case_{i}", "result": "passed"}).encode() + b"\n"
        #     await self.process_output(line) 
        #     await asyncio.sleep(10)


    async def run_tests(self, code):

        self.ticket_obj = await sync_to_async(Ticket.objects.get)(id=self.ticket_id)
        self.result_obj, _ = await sync_to_async(Result.objects.get_or_create)(ticket_id = self.ticket_id)
        
        self.ticket_obj.status = "testing"
        await sync_to_async(self.ticket_obj.save)()

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
                asyncio.create_task(self.read_output(sub_process.stdout)),
                asyncio.create_task(main_task())
            ]

            await asyncio.gather(*tasks)
            await sub_process.wait()

        try:
            await run_subprocess()
            self.ticket_obj.status = "completed"
            await sync_to_async(self.ticket_obj.save)()
            logger.info(f"Ticket {self.ticket_id} marked as completed")
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            self.ticket_obj.status = "error"
            await sync_to_async(self.ticket_obj.save)()
        finally:
            try:
                os.remove(tmp_file_path)
                logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
