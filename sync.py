import os

from datetime import datetime, timezone
from typing import Any


def _get_local_files_info(local_path: str) -> dict[str, float]:
    result = {}

    for entry in os.listdir(local_path):
        full_path = os.path.join(local_path, entry)
        if os.path.isfile(full_path):
            result[entry] = os.path.getmtime(full_path)

    return result


def _handle_remote_only_files(
    connector: Any,
    remote_info: dict[str, str],
    local_info: dict[str, float],
    logger,
) -> None:
    for filename in remote_info:
        if filename in local_info:
            continue
        try:
            connector.delete(filename)
            logger.info(f"Удален из облака: {filename}")
        except Exception as e:
            logger.error(f"Ошибка удаления {filename}: {e}")


def _handle_local_files(
    connector: Any,
    local_path: str,
    remote_info: dict[str, str],
    local_info: dict[str, float],
    logger,
) -> None:
    for filename, local_mtime in local_info.items():
        full_path = os.path.join(local_path, filename)
        if filename not in remote_info:
            _upload_file(connector, full_path, logger)
        else:
            remote_mtime_str = remote_info[filename]
            if _is_local_newer(local_mtime, remote_mtime_str):
                _reupload_file(connector, full_path, logger)


def _upload_file(connector: Any, filepath: str, logger) -> None:
    try:
        connector.load(filepath)
        logger.info(f"Загружен в облако: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Ошибка загрузки {filepath}: {e}")


def _reupload_file(connector: Any, filepath: str, logger) -> None:
    try:
        connector.load(filepath)
        logger.info(f"Перезаписан в облако: {os.path.basename(filepath)}")
    except Exception as e:
        logger.error(f"Ошибка перезаписи {filepath}: {e}")


def _is_local_newer(local_mtime: float, remote_iso: str) -> bool:
    local_dt = datetime.fromtimestamp(local_mtime, tz=timezone.utc)
    remote_dt = datetime.fromisoformat(remote_iso)
    return local_dt > remote_dt


def sync_files(
    connector: Any,
    local_path: str,
    logger,
) -> None:
    try:
        remote_info = connector.get_info()
    except Exception as e:
        logger.error(f"Ошибка получения информации из облака: {e}")
        return

    try:
        local_info = _get_local_files_info(local_path)
    except Exception as e:
        logger.error(f"Ошибка получения информации о файлах в локальном хранилище: {e}")
        return

    _handle_remote_only_files(connector, remote_info, local_info, logger)
    _handle_local_files(connector, local_path, remote_info, local_info, logger)
