from loguru import logger

# Remove the default handler to avoid duplicate logging
logger.remove()

logger.add(
    sink=lambda msg: print(msg.strip()),
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

def get_logger():
    return logger

# HOW TO USE
# from core.logging import logger
# logger.info("This is an info log.")

