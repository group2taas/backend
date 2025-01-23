import logging
from logging.handlers import RotatingFileHandler

class GenericFunctions:

    @staticmethod
    def get_logger(__name__: str, log_level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(filename)s: line %(lineno)d] - %(levelname)s - %(message)s")
        
        #Print logs onto console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        #Store logs into file
        file_handler = RotatingFileHandler("logs/application.log", backupCount = 5, maxBytes = 10000) #adjust if need more per log file
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger