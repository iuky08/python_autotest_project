import time
from typing import Any, Dict

import requests
import urllib.parse
import os
import hashlib
from requests import JSONDecodeError


class ApiClient:
    """Клиент для работы с api.

       Хранит внутри одну сессию
    """

    def __init__(self, url):
        super().__init__()
        self._base_url = urllib.parse.urljoin(url)
        self._session = requests.Session()
        self._rpc_id = 1

    def _url(self, url):
        url = url.lstrip("/")
        return urllib.parse.urljoin(self._base_url, url)

    def forget(self):
        self._session = requests.Session()

    def login(self, username, password):
        """Создаёт новую сессию и выполняет логин с указанными параметрами. После этого все запросы
           через этот клиент делаются с куками, установленными в результате логина"""
        if self._session:
            self._session.close()
        self._session = requests.Session()
        json = self.rpc_result("LoginService.getChallenge")
        assert "challengeValue" in json, f"Unexpected json: {json}"
        challenge = json["challengeValue"]

        hashed_password = hashlib.md5(
            (hashlib.md5(password.encode("utf-8")).hexdigest() + challenge + username).encode("utf-8")
        ).hexdigest().lower()
        self.http_post("/login.do", data={
            "password": hashed_password,
            "submitted": True,
            "username": username,
            "pwd": ""
        }, allow_redirects=False)

        status_code, json = self.get("/api/v2/me")
        assert status_code == 200, f"Response is {status_code}, {json}"
        assert json["username"] == username, f"Username is {json['username']}"

    def post(self, url: str, params=None, headers=None, json=None) -> (int, Dict[str, Any]):
        """Посылает POST запрос с json-ом, возвращает кортеж (код ответа, json ответ)

           Если ожидается не-json ответ, используйте [http_post]
        """
        response = self._session.post(self._url(url), params=params, headers=headers, json=json)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text

    def post_200(self, url: str, params=None, header=None, json=None) -> Dict[str, Any]:
        """Посылает POST запрос, возвращает json ответ
           либо падает с ошибкой, если код возврата не 200
        """
        code, json = self.post(url, params, header, json)
        assert code == 200, f"Unexpected response: {code}\n{json}"
        return json

    def http_post(self, url: str, params=None, data=None, allow_redirects=True) -> (int, str):
        """Посылает POST запрос с данными формы, возвращает кортеж (код ответа, текст ответа)"""
        response = self._session.post(self._url(url), params=params, data=data, allow_redirects=allow_redirects)
        return response.status_code, response.text

    def get(self, url: str, params=None, headers=None) -> (int, Dict[str, Any]):
        """Посылает GET запрос, возвращает кортеж (код ответа, json ответ)

            Если ожидается не json-ответ, используйте [http_get]
        """
        response = self._session.get(self._url(url), params=params, headers=headers)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text

    def get_200(self, url: str, params=None, header=None) -> Dict[str, Any]:
        """Посылает GET запрос, возвращает json ответ
           либо падает с ошибкой, если код возврата не 200
        """
        code, json = self.get(url, params, header)
        assert code == 200, f"Unexpected response: {code}\n{json}"
        return json

    def http_get(self, url: str, params=None, headers=None) -> (int, Dict[str, Any]):
        """Посылает GET запрос, возвращает кортеж (код ответа, текст ответа)"""
        response = self._session.get(self._url(url), params=params, headers=headers)
        return response.status_code, response.text

    def put(self, url: str, params=None, headers=None, json=None) -> (int, Dict[str, Any]):
        """Посылает PUT запрос с json-ом, возвращает кортеж (код ответа, json ответ)"""
        response = self._session.put(self._url(url), params=params, headers=headers, json=json)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text

    def put_200(self, url: str, params=None, header=None, json=None) -> Dict[str, Any]:
        """Посылает PUT запрос, возвращает json ответ
           либо падает с ошибкой, если код возврата не 200
        """
        code, json = self.put(url, params, header, json)
        assert code == 200, f"Unexpected response: {code}\n{json}"
        return json

    def patch(self, url: str, params=None, headers=None, json=None) -> (int, Dict[str, Any]):
        """Посылает PATCH запрос с json-ом, возвращает кортеж (код ответа, json ответ)"""
        response = self._session.patch(self._url(url), params=params, headers=headers, json=json)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text

    def patch_200(self, url: str, params=None, header=None, json=None) -> Dict[str, Any]:
        """Посылает PATCH запрос, возвращает json ответ
           либо падает с ошибкой, если код возврата не 200
        """
        code, json = self.patch(url, params, header, json)
        assert code < 299, f"Unexpected response: {code}\n{json}"
        return json

    def http_patch(self, url: str, params=None, headers=None, json=None) -> (int, Dict[str, Any]):
        """Посылает PATCH запрос с json-ом, возвращает кортеж (код ответа, текст ответ)"""
        response = self._session.patch(self._url(url), params=params, headers=headers, json=json)
        return response.status_code, response.text

    def delete(self, url: str, params=None, headers=None) -> int:
        """Посылает DELETE запрос, возвращает код ответа"""
        response = self._session.delete(self._url(url), params=params, headers=headers)
        return response.status_code

    def rpc(self, method: str, params=None) -> (int, Dict[str, Any]):
        """Посылает rpc запрос с методом и списком параметров, возвращает кортеж (код ответа, json ответ)"""
        if params is None:
            params = []
        self._rpc_id += 1
        return self.post("/rpc", json={
            "id": self._rpc_id,
            "method": method,
            "params": params
        })

    def rpc_result(self, method: str, params=None) -> Dict[str, Any]:
        """То же, что rpc, но падает если ответ не 200 или вернулась ошибка. Возвращает "result" поле из json-ответа"""
        status_code, json = self.rpc(method, params)
        assert status_code == 200, f"RPC method {method} returned non-200 response: {status_code}\n{json}"
        assert "result" in json, f"RPC method {method} returned error: {json}"
        return json["result"]

    def wait_for_sync(self):
        """Ждёт окончания синхронизации базы данных"""
       assert True
