from .delete_remote_files import delete_remote_files
from .handle_local_files import handle_local_files
from .local_files_info import get_local_files_info


def sync_files(
    connector,
    local_path: str,
    logger,
) -> None:
    """Выполняет один цикл синхронизации файлов.

    Сравнивает состояние локальной папки и облачного хранилища,
    выполняет загрузку новых/изменённых файлов и удаление отсутствующих.

    Args:
        connector: Объект класса-коннектора к облачному хранилищу.
        local_path: Путь к отслеживаемой локальной папке.
        logger: Настроенный объект логгера.
    """
    try:
        remote_info = connector.get_info()
    except Exception as e:
        logger.error(f"Ошибка получения информации из облака: {e}")
        print(f"Ошибка получения информации из облака: {e}")
        return

    try:
        local_info = get_local_files_info(local_path)
    except Exception as e:
        logger.error(f"Ошибка получения информации о файлах в локальном хранилище: {e}")
        print(f"Ошибка получения информации о файлах в локальном хранилище: {e}")
        return

    delete_remote_files(connector, remote_info, local_info, logger)
    handle_local_files(connector, local_path, remote_info, local_info, logger)
