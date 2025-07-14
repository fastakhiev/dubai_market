import datetime
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from ormar.exceptions import NoMatch
from app.core.ban_cache import ban_cache
from app.models.users import User  # поправьте под ваш путь


class BanMiddleware(BaseMiddleware):
    """
    Блокирует пользователей, у которых в БД is_active=False.
    - Кеширует результат проверки на cachetools.TTLCache.
    - При промахе кеша — делает запрос к Ormar (Postgres).
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            # если это не апдейт от пользователя, просто пропускаем
            return await handler(event, data)

        telegram_id = str(user.id)

        # Пытаемся взять флаг из кеша
        is_active = ban_cache.get(telegram_id)
        if is_active is None:
            # Кеш-промах — читаем из БД
            try:
                user_obj = await User.objects.get(telegram_id=str(telegram_id))
                is_active = user_obj.is_active
            except NoMatch:
                # Если пользователя нет в БД, считаем его активным (или меняйте логику)
                is_active = True

            # Записываем в кеш
            ban_cache[telegram_id] = is_active

        if not is_active:
            # Пользователь заблокирован
            if hasattr(event, "answer"):
                await event.answer("🚫 Извините, вы заблокированы.")
            return  # прерываем дальнейшую обработку

        # Всё хорошо — пропускаем дальше
        return await handler(event, data)