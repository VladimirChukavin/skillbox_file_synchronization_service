import os


def reupload_file(connector, filepath: str, logger) -> None:
    """Перезаписывает изменённый файл в облачном хранилище.

    Args:
        connector: Объект класса-коннектора к облачному хранилищу.
        filepath: Путь к файлу на локальном компьютере.
        logger: Настроенный объект логгера.
    """
    try:
        connector.reload(filepath)
        logger.info(f"Перезаписан в облако: {os.path.basename(filepath)}")
    except FileNotFoundError as e:
        logger.error(f"Ошибка перезаписи {filepath}: {e}")
