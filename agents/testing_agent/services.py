import tempfile
import subprocess
import os
from loguru import logger
import threading

class TestingAgent:
    def __init__(self):    
        pass

    def process_output(self, line):
        logger.info(f"Subprocess output: {line}")

    def read_output(self, sub_process):
        while sub_process.poll() is None:
            line = sub_process.stdout.readline()
            self.process_output(line)

    def run_tests(self, code):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        logger.info(f"Temporary test file created at: {tmp_file_path}")

        try:
            sub_process = subprocess.Popen(
                ["python", "-u", tmp_file_path],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True
            )
            
            thread = threading.Thread(target = self.read_output, args = (sub_process,))
            thread.start()

            logger.info("Main process starts")
            
            sub_process.wait()
            thread.join()

        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
                logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
