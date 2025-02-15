import tempfile
import asyncio
import os
# from loguru import logger
# from base.model_handler import AIModelHandler
# from .prompts import TEST_CASE_GENERATION_PROMPT

class TestingAgent:
    def __init__(self):    
        pass

    async def process_output(self, line):
            print(f"Subprocess output: {line.decode().strip()}")

    async def read_output(self, stream, callback):
        while True:
            line = await stream.readline()
            await self.process_output(line)
            if not line:
                break
            # callback(line.decode().strip())

    def generate_test_cases_from_code(self, code):
        pass


    def run_tests(self, code):
        
        self.generate_test_cases_from_code(code)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        print(f"Temporary test file created at: {tmp_file_path}")

        async def main_task():
            for i in range(10):
                print(f"Main task iteration {i}")
                await asyncio.sleep(1)

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

        except Exception as e:
            print(f"Failed to run tests: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
                print("Temporary test file removed")
            except Exception as e:
                print(f"Failed to remove temporary file: {e}")


if __name__ == "__main__":
    agent = TestingAgent()
    agent.run_tests("""\
import time
for i in range(100):
    print(i)
    time.sleep(3)
""")