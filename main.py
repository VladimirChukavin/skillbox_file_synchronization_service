import os
import time

from config_utilities.setup_config import setup_config
from config_utilities.setup_logger import setup_logger
from connecting_storage.yandex_disk_connecting import YandexDiskConnector
from sync_utilities.sync_files import sync_files


def main() -> None:
    """Запускает приложение синхронизации файлов.

    Настраивает конфигурацию, логгер, создаёт коннектор к облаку
    и запускает бесконечный цикл синхронизации.
    Завершается по нажатию Ctrl+C.
    """
    config_path = os.path.join(os.path.dirname(__file__), ".env")
    config = setup_config(config_path)
    logger = setup_logger(config["LOG_FILE_PATH"])

    logger.info("Запуск приложения")
    logger.info(f"Синхронизируемая папка: {config['SYNC_FOLDER_PATH']}")

    connector = YandexDiskConnector(
        token=config["YANDEX_TOKEN"],
        folder_name=config["CLOUD_FOLDER_NAME"],
    )

    sync_interval = int(config["SYNC_INTERVAL"])

    sync_files(connector, config["SYNC_FOLDER_PATH"], logger)

    try:
        while True:
            time.sleep(sync_interval)
            sync_files(connector, config["SYNC_FOLDER_PATH"], logger)
    except KeyboardInterrupt:
        logger.info("Завершение работы приложения")


if __name__ == "__main__":
    main()
