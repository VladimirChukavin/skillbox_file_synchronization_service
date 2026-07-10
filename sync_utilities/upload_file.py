import os


def upload_file(connector, filepath: str, logger) -> None:
    """Загружает новый файл в облачное хранилище.

    Args:
        connector: Объект класса-коннектора к облачному хранилищу.
        filepath: Путь к файлу на локальном компьютере.
        logger: Настроенный объект логгера.
    """
    try:
        connector.load(filepath)
        logger.info(f"Загружен в облако: {os.path.basename(filepath)}")
        print(f"Загружен в облако: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Ошибка загрузки {filepath}: {e}")
        print(f"Ошибка загрузки {filepath}: {e}")
