import os
import sys


def validate_local_folder(folder_path: str) -> None:
    """Проверяет существование локальной папки.

    Args:
        folder_path: Путь к проверяемой папке.

    Raises:
        SystemExit: Если папка не существует.
    """
    if not os.path.isdir(folder_path):
        print(f'Ошибка: папка "{folder_path}" не существует.')
        sys.exit(1)
