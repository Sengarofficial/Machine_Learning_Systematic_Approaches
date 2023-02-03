import logging

from datetime import datetime 
from pathlib import Path 
from typing import Optional 

class RootLoggerManager:

    # Logging.Formatter(s) that can be used by handlers 

    MINIMAL_FORMATTER = logging.Formatter(
        "[%(levelname)s %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    BASIC_FORMATTER = logging.Formatter(
        "[%(asctime)s] %(levelname)s -- : %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    VERBOSE_FORMATTER = logging.Formatter(
        "[%(asctime)s] (module=%(module)s func=%(funcName)s %(levelname)s -- : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    def __init__(self):

        # Initialiization Process 
        # logging.getLogger() returns a reference to a logger instance with specified name 
        # if it is provided, or root if not. 
        self.logger = logging.getLogger()

        self.logger.setLevel(logging.INFO)

        # Remove handlers because others libraries may already define some of them 
        # (i.e streamlit, requests)

        self.logger.handlers = []

    def Configure(

        self, output_path: Optional[Path] = None 
    ): 

        """
        Configure the root logger's handlers and their verbosity. 

        Args:
            output_path (Optional, optional): The output path used by 'FileHandler'. 
        """

        # Setup the console logging 
        self.set_console_logging(self.BASIC_FORMATTER)

        # If the output log path is provided than initiate the file logging  

        if output_path:
            self.set_file_logging(path=output_path, formatter=self.VERBOSE_FORMATTER)

    def set_console_logging(self, formatter: logging.Formatter):

        """
        Add a "Streamhandler" to the root logger (for console logging).

        Args: 
        formatter (logging.Formatter): The logging formatter that will be used 
        """

        handler = logging.Streamhandler()

        # set logging format

        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        # Add handler to logger 

        self.logger.addHandler(handler)

    def set_file_logging(self, path: Path, formatter: logging.Formatter):

        """Add a FileHandler to the Logger (for file logging).

        Args: 
        path (Path): The output path 
        formatter (logging.Formattter): The logging formatter that will be used. 

        """

        # If parent folders do not exist just create them 

        filename = path / f"{datetime.now().strftime('Y%m%d-%H%M%S')}.log"

        try:
            filename.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(filename, "w")

            # Make sure that the file now exists 
            assert filename.exists()

        except Exception as e:
            logging.critical(
                f"Unable to create the file in order to store the output logs: {e}."
            )

        # Set logging format 
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)


        # Add Handler to logger 
        self.logger.addHandler(handler)

logger_manager = RootLoggerManager()
logger_manager.configure(Path('./logs'))
logger = logger_manager.logger # Renaming logger as logger_manager for simplicity 



    