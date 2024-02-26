import datetime
import os


def get_bool_env_variable(var_name: str) -> bool:
    return os.environ.get(var_name, '').lower() in ("true", "1", 't')


def unix_time_millis(dt: datetime.datetime) -> int:
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds()) * 1000
