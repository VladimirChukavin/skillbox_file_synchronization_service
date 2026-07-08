from loguru import logger


def setup_logger(log_file_path: str):
    """Настраивает логгер loguru для записи в файл.

    Удаляет все предыдущие обработчики и добавляет новый,
    который записывает логи в указанный файл.

    Args:
        log_file_path: Путь к файлу для записи логов.

    Returns:
        Настроенный объект логгера loguru.
    """
    logger.remove()
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        rotation="10 MB",
        encoding="utf-8",
    )
    return logger
