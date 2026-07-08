import os


def get_local_files_info(local_path: str) -> dict[str, float]:
    """Собирает информацию о файлах в локальной директории.

    Args:
        local_path: Путь к отслеживаемой папке.

    Returns:
        Словарь вида {имя_файла: время_последнего_изменения}.
        Время возвращается как float.
    """
    result = {}

    for entry in os.listdir(local_path):
        full_path = os.path.join(local_path, entry)
        if os.path.isfile(full_path):
            result[entry] = os.path.getmtime(full_path)

    return result
