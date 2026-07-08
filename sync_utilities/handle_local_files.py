import os

from .upload_file import upload_file
from .reupload_file import reupload_file
from .compare_local_and_remote_files import is_local_newer


def handle_local_files(
    connector,
    local_path: str,
    remote_info: dict[str, str],
    local_info: dict[str, float],
    logger,
) -> None:
    """Загружает новые или обновляет изменённые локальные файлы в облако.

    Args:
        connector: Объект класса-коннектора к облачному хранилищу.
        local_path: Путь к отслеживаемой локальной папке.
        remote_info: Словарь с информацией о файлах в облаке.
        local_info: Словарь с информацией о локальных файлах.
        logger: Настроенный объект логгера.
    """
    for filename, local_mtime in local_info.items():
        full_path = os.path.join(local_path, filename)
        if filename not in remote_info:
            upload_file(connector, full_path, logger)
        else:
            remote_mtime_str = remote_info[filename]
            if is_local_newer(local_mtime, remote_mtime_str):
                reupload_file(connector, full_path, logger)
