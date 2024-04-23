#region DEPENDENCIES
import os
import sys
import logging
import multiprocessing_logging

from util import file_util
from constants.logger_constants import *
#endregion

LOGGER_CONFIG = {
    'level': 'INFO',
    'log_file': 'logs/wordle.log'
}

def configure_logger(reset_log_file=False) -> logging.Logger:
    LOGGER_LEVEL = LOGGER_CONFIG['level']
    LOGGER_FILE = LOGGER_CONFIG['log_file']

    if reset_log_file and file_util.file_exists(LOGGER_FILE):
        os.remove(LOGGER_FILE)
        
    logger = logging.getLogger()
    if logger.hasHandlers():
        # Logger already configured, skipping redundant call due to multiprocessing
        return
    
    logger.setLevel(logging.getLevelName(LOGGER_LEVEL))
    logger.addHandler(_get_file_handler(LOGGER_FILE))
    # logger.addHandler(get_console_handler())

    multiprocessing_logging.install_mp_handler(logger)

#region FILTERS
class _RemoveTQDMLog(logging.Filter):
    def filter(self, record):
        # If `tqdm_log` is True then do not log it`
        return not getattr(record, LOGGER_EXTRA_TQDM_LOG, False)
    
class _StepHeader(logging.Filter):
    def filter(self, record):
        record.msg_console = record.msg
        if getattr(record, LOGGER_EXTRA_STEP_HEADER, False):
            record.msg_console = f'{COLOR_GREEN}{BOLD}{record.msg}{RESET_ALL}'
            record.msg_console = '\033[1;32m' + record.msg + '\033[0m'
        return True
#endregion

#region HANDLERS
def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(CLI_LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT))
    console_handler.addFilter(_RemoveTQDMLog())
    console_handler.addFilter(_StepHeader())
    return console_handler

def _get_file_handler(logger_file):
    file_handler = logging.FileHandler(filename=logger_file)
    file_handler.setFormatter(logging.Formatter(FILE_LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT))
    return file_handler
#endregion
