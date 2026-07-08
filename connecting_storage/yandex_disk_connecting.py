import os

import requests


class YandexDiskConnector:
    """Класс-коннектор для работы с API Яндекс Диск.

    Заключает всю логику взаимодействия с облачным хранилищем:
    загрузку, перезапись, удаление файлов и получение информации
    о хранящихся файлах.

    Attributes:
        BASE_URL: Базовый URL API Яндекс Диск.
    """

    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token: str, folder_name: str) -> None:
        """Инициализирует коннектор к Яндекс Диск.

        Args:
            token: OAuth-токен доступа к Яндекс Диск.
            folder_name: Имя директории в облаке для хранения бэкапов.
        """
        self._token = token
        self._folder_name = folder_name
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"OAuth {self._token}",
                "Content-Type": "application/json",
            }
        )

    def _ensure_folder(self) -> None:
        """Создаёт папку на Яндекс Диск, если она не существует.

        Метод идемпотентен — повторный вызов не создаёт дубликатов.
        """
        url = f"{self.BASE_URL}?path=app:/{self._folder_name}"
        self._session.put(url, timeout=30)

    def _get_upload_href(self, filename: str) -> str:
        """Получает временную ссылку для загрузки файла.

        Выполняет GET-запрос к API для получения временной ссылки
        (href), на которую затем можно отправить PUT-запрос с файлом.

        Args:
            filename: Имя файла для загрузки.

        Returns:
            Временная ссылка (URL) для загрузки файла.

        Raises:
            requests.HTTPError: Если запрос к API завершился ошибкой.
        """
        url = f"{self.BASE_URL}/upload?path=app:/{self._folder_name}/{filename}&overwrite=true"
        response = self._session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()["href"]

    def get_info(self) -> dict[str, str]:
        """Получает информацию о файлах в облачной папке.

        Возвращает словарь, где ключ — имя файла, а значение —
        время последнего изменения в формате ISO 8601.

        Returns:
            Словарь вида {имя_файла: время_изменения}.
        """
        self._ensure_folder()

        url = (
            f"{self.BASE_URL}"
            f"?path=app:/{self._folder_name}"
            f"&fields=_embedded.items.name,_embedded.items.modified"
        )
        response = self._session.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        result = {}

        items = data.get("_embedded", {}).get("items", [])

        for item in items:
            name = item.get("name", "")
            modified = item.get("modified", "")
            result[name] = modified

        return result

    def load(self, filepath: str) -> None:
        """Загружает файл в облачное хранилище.

        Выполняет двухшаговую загрузку: сначала получает временную
        ссылку через GET-запрос, затем отправляет файл через PUT.

        Args:
            filepath: Путь к файлу на локальном компьютере.

        Raises:
            requests.HTTPError: Если загрузка завершилась ошибкой.
        """
        filename = os.path.basename(filepath)

        href = self._get_upload_href(filename)

        with open(filepath, "rb") as file:
            response = self._session.put(href, data=file, timeout=60)
            response.raise_for_status()

    def reload(self, filepath: str) -> None:
        """Перезаписывает файл в облачном хранилище.

        Переиспользует метод load(), так как API поддерживает
        перезапись по умолчанию.

        Args:
            filepath: Путь к файлу на локальном компьютере.
        """
        self.load(filepath)

    def delete(self, filename: str) -> None:
        """Удаляет файл из облачного хранилища.

        Args:
            filename: Имя файла для удаления.

        Raises:
            requests.HTTPError: Если удаление завершилось ошибкой.
        """
        url = f"{self.BASE_URL}?path=app:/{self._folder_name}/{filename}"
        response = self._session.delete(url, timeout=30)
        response.raise_for_status()
