from generics import GenericFunctions as g

if __name__ == "__main__":
    # Using the logger
    logger = g.get_logger("logging_test")
    for _ in range(50):
        #order of severity: DEBUG, INFO, WARNING, ERROR, CRITICAL
        logger.debug("THIS IS DEBUG")
        logger.info("THIS IS INFO")
        logger.warning("THIS IS WARNING")
        logger.error("THIS IS ERROR")
        logger.critical("THIS IS CRITICAL")