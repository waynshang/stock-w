import logging

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    color = {
      "green": "\x1b[1;32m",
      "blue": "\x1b[1;34m",
      "light_blue" : "\x1b[1;36m",
      "grey": "\x1b[38;21m",
      "white": "\x1b[37;21m",
      "yellow": "\x1b[33;21m",
      "red": "\x1b[31;21m",
      "bold_red": "\x1b[31;1m",
      "reset": "\x1b[0m",
    }
    
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # 2021-07-10 12:33:34,468 - stock - DEBUG - test (log.py:38)
    format = "%(asctime)s - %(levelname)s: "
    formatContext = "%(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: color["green"] + format,
        logging.INFO: color["blue"] + format,
        logging.WARNING: color["yellow"] + format,
        logging.ERROR: color["red"]  + format,
        logging.CRITICAL: color["bold_red"] + format,
    }
    CONTEXT_FORMATS = {
      "default": color["white"] + formatContext + color["reset"],
    }

    def format(self, record):
      log_fmt = self.FORMATS.get(record.levelno)
      log_context_fmt = self.CONTEXT_FORMATS.get("default")
      formatter = logging.Formatter(log_fmt+log_context_fmt)
      return formatter.format(record)

# class DebugLog():
#   def __init__(self):

#     self.__logger = logging.getLogger("stock")
#     self.__logger.setLevel(logging.DEBUG)
#     # create console handler with a higher log level
#     ch = logging.StreamHandler()
#     ch.setLevel(logging.DEBUG)
#     ch.setFormatter(CustomFormatter())
#     self.__logger.addHandler(ch)
  
#   def getLogger(self):
#     DEBUG.info("123123")
#     return self.__logger
LOGGER = logging.getLogger("stock")
LOGGER.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
LOGGER.addHandler(ch)

def getLogger():
  return LOGGER
