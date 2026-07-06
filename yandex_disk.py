import os

import requests


class YandexDiskConnector:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token: str, folder_name: str) -> None:
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
        url = f"{self.BASE_URL}?path=app:/{self._folder_name}"
        self._session.put(url, timeout=30)

    def _get_upload_href(self, filename: str) -> str:
        url = f"{self.BASE_URL}/upload?path=app:/{self._folder_name}/{filename}&overwrite=true"
        response = self._session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()["href"]

    def get_info(self) -> dict[str, str]:
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
        filename = os.path.basename(filepath)

        href = self._get_upload_href(filename)

        with open(filepath, "rb") as file:
            response = self._session.put(href, data=file, timeout=60)
            response.raise_for_status()

    def reload(self, filepath: str) -> None:
        self.load(filepath)

    def delete(self, filename: str) -> None:
        url = f"{self.BASE_URL}?path=app:/{self._folder_name}/{filename}"
        response = self._session.delete(url, timeout=30)
        response.raise_for_status()
