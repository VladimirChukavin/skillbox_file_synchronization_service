import sys

from connecting_storage.yandex_disk_connecting import YandexDiskConnector


def validate_token(config: dict[str, str]) -> None:
    """Проверяет валидность токена доступа к Яндекс Диск.

    Выполняет тестовый запрос к API для проверки токена.

    Args:
        config: Словарь с настройками конфигурации.

    Raises:
        SystemExit: Если токен недействителен.
    """
    connector = YandexDiskConnector(
        token=config["YANDEX_TOKEN"],
        folder_name=config["CLOUD_FOLDER_NAME"],
    )

    try:
        connector.get_info()
    except Exception as e:
        print(f"Ошибка: недействительный токен доступа к Яндекс Диск.\n {e}")
        sys.exit(1)
