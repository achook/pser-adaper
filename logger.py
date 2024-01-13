def log_info(msg: str):
    print("INFO:  " + msg)


def log_warning(msg: str):
    print("WARN:  " + msg)


def log_error(msg: str):
    print("ERROR: " + msg)


def log_fatal(msg: str, exit_code: int = 1):
    print("FATAL: " + msg)
    print("Exiting with code: " + str(exit_code))
    exit(1)
