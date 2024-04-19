RESET_ALL = "\033[0m"

COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
BOLD = "\033[1m"

LOGGER_NAME = 'MAIN'
CLI_LOGGER_FORMAT = (
    f"{COLOR_CYAN}%(asctime)s{RESET_ALL} "
    f"{COLOR_GREEN}%(processName)-4s{RESET_ALL} "
    f"{COLOR_MAGENTA}{BOLD}%(levelname)-4s{RESET_ALL} "
    f"{COLOR_YELLOW}[%(filename)s:%(lineno)d]{RESET_ALL} "
    f"{COLOR_WHITE}%(msg_console)s{RESET_ALL}"
)
FILE_LOGGER_FORMAT = '%(asctime)s %(processName)-4s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LOGGER_EXTRA_TQDM_LOG = 'tqdm_log'
LOGGER_EXTRA_STEP_HEADER = 'step_header'
