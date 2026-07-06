import os
import sys
import time

from dotenv import dotenv_values
from loguru import Logger, logger as loguru_logger

from sync import sync_files
from yandex_disk import YandexDiskConnector


def _validate_config(config: dict[str, str | None]) -> dict[str, str]:
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


def _validate_local_folder(folder_path: str) -> None:
    if not os.path.isdir(folder_path):
        print(f'Ошибка: папка "{folder_path}" не существует.')


def _validate_token(config: dict[str, str]) -> None:
    connector = YandexDiskConnector(
        token=config["YANDEX_TOKEN"],
        folder_name=config["CLOUD_FOLDER_NAME"],
    )

    try:
        connector.get_info()
    except Exception as e:
        print("Ошибка: недействительный токен доступа к Яндекс Диск.")
        sys.exit(1)


def setup_config() -> dict[str, str]:
    config_path = os.path.join(os.path.dirname(__file__), ".env")
    raw_config = dotenv_values(config_path)
    config = _validate_config(raw_config)
    _validate_local_folder(config["SYNC_FOLDER_PATH"])
    _validate_token(config)
    return config


def setup_logger(log_file_path: str) -> Logger:
    loguru_logger.remove()
    loguru_logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        rotation="10 MB",
        encoding="utf-8",
    )
    return loguru_logger


def main() -> None:
    config = setup_config()
    logger = setup_logger(config["LOG_FILE_PATH"])

    logger.info("Запуск приложения")
    logger.info(f"Синхронизируемая папка: {config['SYNC_FOLDER_PATH']}")

    connector = YandexDiskConnector(
        token=config["YANDEX_TOKEN"],
        folder_name=config["CLOUD_FOLDER_NAME"],
    )

    sync_interval = int(config["SYNC_INTERVAL"])

    sync_files(connector, config["SYNC_FOLDER_PATH"], logger)

    while True:
        time.sleep(sync_interval)
        sync_files(connector, config["SYNC_FOLDER_PATH"], logger)


if __name__ == "__main__":
    main()
