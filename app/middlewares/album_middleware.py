import asyncio
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from collections import defaultdict
from typing import Callable, Dict, Awaitable, Any


class AlbumMiddleware(BaseMiddleware):
    """Middleware для сбора всех фото в альбоме"""

    def __init__(self):
        super().__init__()
        self.albums = defaultdict(list)
        self.queues = defaultdict(asyncio.Queue)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        media_group_id = event.media_group_id

        if media_group_id:
            self.albums[media_group_id].append(event)

            await asyncio.sleep(1)

            if len(self.albums[media_group_id]) > 1:
                data["album"] = self.albums.pop(media_group_id, [])
                return await handler(event, data)

            return

        return await handler(event, data)
