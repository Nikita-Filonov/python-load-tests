import time

from httpx import Request, Response, HTTPStatusError, HTTPError
from locust.env import Environment


def locust_request_event_hook(request: Request) -> None:
    request.extensions["start_time"] = time.time()


def locust_response_event_hook(environment: Environment):
    def inner(response: Response) -> None:
        exception: HTTPError | HTTPStatusError | None = None

        try:
            response = response.raise_for_status()
        except (HTTPError, HTTPStatusError) as error:
            exception = error

        request = response.request

        route = request.extensions.get("route", request.url.path)
        start_time = request.extensions.get("start_time", time.time())
        response_time = (time.time() - start_time) * 1000
        response_length = len(response.read())

        environment.events.request.fire(
            name=f"{request.method} {route}",
            context=None,
            response=response,
            exception=exception,
            request_type="HTTP",
            response_time=response_time,
            response_length=response_length,
        )

    return inner
