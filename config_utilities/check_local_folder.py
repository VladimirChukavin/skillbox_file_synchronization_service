import os
import sys


def validate_local_folder(folder_path: str, logger) -> None:
    """Проверяет существование локальной папки.

    Args:
        folder_path: Путь к проверяемой папке.
        logger: Настроенный объект логгера.

    Raises:
        SystemExit: Если папка не существует.
    """
    if not os.path.isdir(folder_path):
        logger.error(f'Ошибка: папка "{folder_path}" не существует.')
        sys.exit(1)
