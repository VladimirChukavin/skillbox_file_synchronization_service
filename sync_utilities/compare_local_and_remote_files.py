from datetime import datetime, timezone


def is_local_newer(local_mtime: float, remote_iso: str) -> bool:
    """Сравнивает время изменения локального и удалённого файлов.

    Args:
        local_mtime: Время последнего изменения локального файла
                     (float).
        remote_iso: Время изменения облачного файла в формате
                    ISO 8601 (строка).

    Returns:
        True, если локальный файл новее облачного, иначе False.
    """
    local_dt = datetime.fromtimestamp(local_mtime, tz=timezone.utc)
    remote_dt = datetime.fromisoformat(remote_iso)
    return local_dt > remote_dt
