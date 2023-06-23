# a logger module to log the process and error messages and save the log file.
import logging


class Logger():
    """
    Create logger class to log the information, and save the log file
    Create logger class to log the information, and save the log file"""
    def __init__(self, log_file: str, log_level: str = "INFO"):
        """
        Create logger class to log the information, and save the log file
        
        Args:
            log_file (str): log file name
            log_level (str): log level
        """
        self.log_file:str = log_file
        self.log_level:str = log_level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        self.formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        self.file_handler = logging.FileHandler(self.log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        
    def log(self, msg: str, level: str = "INFO"):
        """
        Log message
        
        Args:
            msg (str): message
            level (str): log level
        """
        if level == "INFO":
            self.logger.info(msg)
        elif level == "DEBUG":
            self.logger.debug(msg)
        elif level == "WARNING":
            self.logger.warning(msg)
        elif level == "ERROR":
            self.logger.error(msg)
        elif level == "CRITICAL":
            self.logger.critical(msg)
        else:
            self.logger.info(msg)
        return None