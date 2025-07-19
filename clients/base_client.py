import logging
from typing import Any, TypedDict

from httpx import Client, URL, Response, QueryParams
from locust.env import Environment

from clients.event_hooks import locust_request_event_hook, locust_response_event_hook
from config import HTTPClientConfig


class ClientExtensions(TypedDict, total=False):
    route: str


class BaseClient:
    def __init__(self, client: Client):
        self.client = client

    def get(
            self,
            url: URL | str,
            params: QueryParams | None = None,
            extensions: ClientExtensions | None = None
    ) -> Response:
        return self.client.get(url, params=params, extensions=extensions)

    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            extensions: ClientExtensions | None = None
    ) -> Response:
        return self.client.post(url, json=json, extensions=extensions)


def get_http_client(config: HTTPClientConfig) -> Client:
    return Client(timeout=config.timeout, base_url=config.client_url)


def get_locust_http_client(config: HTTPClientConfig, environment: Environment) -> Client:
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    return Client(
        timeout=config.timeout,
        base_url=config.client_url,
        event_hooks={
            "request": [locust_request_event_hook],
            "response": [locust_response_event_hook(environment)]
        }
    )
