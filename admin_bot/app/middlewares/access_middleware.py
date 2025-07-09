from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class AdminAccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: set[int]):
        self.allowed_ids = allowed_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user and user.id in self.allowed_ids:
            return await handler(event, data)

        # Не показываем сообщения тем, кто не в списке
        if hasattr(event, "answer"):
            await event.answer("⛔ У вас нет доступа к этому боту.")
        return  # Прерываем выполнение