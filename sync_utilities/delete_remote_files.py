from requests import exceptions


def delete_remote_files(
    connector,
    remote_info: dict[str, str],
    local_info: dict[str, float],
    logger,
) -> None:
    """Удаляет из облака файлы, которых нет в локальной папке.

    Args:
        connector: Объект класса-коннектора к облачному хранилищу.
        remote_info: Словарь с информацией о файлах в облаке.
        local_info: Словарь с информацией о локальных файлах.
        logger: Настроенный объект логгера.
    """
    for filename in remote_info:
        if filename in local_info:
            continue
        try:
            connector.delete(filename)
            logger.info(f"Удален из облака: {filename}")
        except exceptions.HTTPError as e:
            logger.error(f"Ошибка удаления {filename}: {e}")
