from typing import Any
from typing import List
from typing import Optional

from aiohttp import AsyncResolver
from aiohttp import TCPConnector
from aiohttp_retry import ExponentialRetry
from aiohttp_retry import RetryClient
from aiohttp_retry import RetryOptionsBase
from aiohttp_retry.client import _Logger
import logging

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)


class RetryClientSession(RetryClient):
    def __init__(
        self,
        logger: Optional[_Logger] = logger,
        dns_tries: int = 4,
        dns_timeout: float = 5.0,
        http_attempts: int = 3,
        http_start_timeout: float = 0.1,
        http_max_timeout: float = 30.0,
        http_backoff_factor: float = 2.0,
        http_retry_statuses: Optional[List[str]] = None,
        raise_for_status: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if http_retry_statuses is not None:
            http_retry_statuses = [int(status) for status in http_retry_statuses]
        retry_options: RetryOptionsBase = ExponentialRetry(
            attempts=http_attempts,
            start_timeout=http_start_timeout,
            max_timeout=http_max_timeout,
            factor=http_backoff_factor,
            statuses=http_retry_statuses,
        )
        resolver = AsyncResolver(
            tries=dns_tries,
            timeout=dns_timeout,
        )
        tcp_connector = TCPConnector(resolver=resolver)
        kwargs.setdefault("connector", tcp_connector)
        super().__init__(
            None,
            logger,
            retry_options,
            raise_for_status,
            *args,
            **kwargs,
        )
