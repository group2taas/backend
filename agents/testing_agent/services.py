import tempfile
import asyncio
import os
from loguru import logger
from base.model_handler import AIModelHandler
from .prompts import TEST_CASE_GENERATION_PROMPT

class TestingAgent:
    def __init__(self):    
        pass

    async def process_output(self, line):
            cleaned_line = line.decode().strip()
            logger.info(f"Subprocess output: {cleaned_line}")

    async def read_output(self, stream, callback):
        while True:
            line = await stream.readline()
            await self.process_output(line)
            if not line:
                break

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
            sub_process = asyncio.create_subprocess_exec(
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

        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
                logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
