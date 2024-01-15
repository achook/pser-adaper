def log_info(msg: str) -> None:
    print("INFO:  " + msg)


def log_warning(msg: str) -> None:
    print("WARN:  " + msg)


def log_error(msg: str) -> None:
    print("ERROR: " + msg)


def log_fatal(msg: str, exit_code: int = 1) -> None:
    print("FATAL: " + msg)
    print("Exiting with code: " + str(exit_code))
    exit(1)
