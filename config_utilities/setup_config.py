from dotenv import dotenv_values

from .check_local_folder import validate_local_folder
from .check_required_keys_in_configuration import validate_keys_in_config
from .check_token import validate_token


def setup_config(config_path) -> dict[str, str]:
    """Загружает и проверяет конфигурацию из файла .env.

    Args:
        config_path: Путь к файлу .env.

    Returns:
        Словарь с проверенными настройками конфигурации.
    """
    raw_config = dotenv_values(config_path)
    config = validate_keys_in_config(raw_config)
    validate_local_folder(config["SYNC_FOLDER_PATH"])
    validate_token(config)
    return config
