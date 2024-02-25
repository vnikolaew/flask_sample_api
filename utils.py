import os


def get_bool_env_variable(var_name: str) -> bool:
    return os.environ.get(var_name, '').lower() in ("true", "1", 't')
