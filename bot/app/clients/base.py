from typing import Any
from typing import Literal
from typing import Optional
from typing import Tuple

from aiohttp import ContentTypeError

from app.clients.exceptions import BadRequestAPIException
from app.clients.exceptions import ClientErrorAPIException
from app.clients.exceptions import ServerErrorAPIException
from app.common.utils.session import RetryClientSession
from app.core import config


__all__ = [
    "BaseAPI",
]


class BaseAPI:
    base_url: str = None

    @classmethod
    async def _request(
        cls,
        method: Literal["get", "post", "put", "patch", "delete"],
        path: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json_data: Optional[Any] = None,
    ) -> Tuple[int, Any]:
        _url = f"{cls.base_url}{path}"
        _headers = {
            "Content-Type": "application/json",
        }

        if headers:
            _headers.update(headers)

        _params = params or {}
        _json = json_data or {}

        async with RetryClientSession() as session:
            _session_method = getattr(session, method)
            async with _session_method(
                url=_url,
                headers=_headers,
                params=_params,
                json=_json,
            ) as response:
                if response.status == 400:
                    raise BadRequestAPIException(
                        response.status,
                    )
                elif 400 < response.status <= 499:
                    raise ClientErrorAPIException(
                        response.status,
                    )

                elif response.status >= 500:
                    raise ServerErrorAPIException(response.status, response._body)
                try:
                    response_json = await response.json()
                except ContentTypeError:
                    response_json = {}

        return response.status, response_json
