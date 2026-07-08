import sys


def validate_keys_in_config(config: dict[str, str | None]) -> dict[str, str]:
    """Проверяет наличие обязательных ключей в конфигурации.

    Args:
        config: Словарь с настройками из файла .env.

    Returns:
        Словарь с проверенными настройками, значения которых
        приведены к строковому типу.

    Raises:
        SystemExit: Если отсутствуют обязательные ключи.
    """
    required_keys = [
        "SYNC_FOLDER_PATH",
        "CLOUD_FOLDER_NAME",
        "YANDEX_TOKEN",
        "SYNC_INTERVAL",
        "LOG_FILE_PATH",
    ]
    missing = [key for key in required_keys if not config.get(key)]

    if missing:
        print(
            f"Ошибка в файле .env не заданы обязательные параметры: "
            f"{', '.join(missing)}.\n"
        )
        sys.exit(1)

    return {key: str(config[key]) for key in required_keys}
