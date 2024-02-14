import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)

c_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s')
c_handler.setFormatter(c_format)

logger.addHandler(c_handler)
