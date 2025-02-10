import tempfile
import subprocess
import os
from loguru import logger

class TestingAgent:
    def __init__(self):    
        pass

    def run_tests(self, code):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file_path = tmp_file.name

        logger.info(f"Temporary test file created at: {tmp_file_path}")

        try:
            result = subprocess.run(
                ["python", tmp_file_path],
                capture_output=True,
                text=True
            )
            logger.info(f"Test output:\n{result.stdout}")
            if result.stderr:
                logger.error(f"Test error output:\n{result.stderr}")
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
                logger.info("Temporary test file removed")
            except Exception as e:
                logger.error(f"Failed to remove temporary file: {e}")
