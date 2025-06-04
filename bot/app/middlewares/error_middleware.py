from aiogram import BaseMiddleware
from aiogram.types import Update, Message
from aiogram.exceptions import TelegramBadRequest
from app.handlers.v1.sign_up import cmd_start
from app.core.bot import bot
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any
from aiogram.dispatcher.dispatcher import Dispatcher


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except TelegramBadRequest as exception:
            error_text = str(exception)

            if (
                "message can't be edited" in error_text
                or "message to edit not found" in error_text
                or "message can't be deleted for everyone" in error_text
            ):
                if event.callback_query:
                    user = event.callback_query.from_user
                    chat = event.callback_query.message.chat
                    message_id = event.callback_query.message.message_id

                    fake_message = Message(
                        message_id=message_id,
                        date=event.callback_query.message.date,
                        chat=chat,
                        from_user=user,
                        text="/start"
                    ).as_(bot)

                    dp: Dispatcher = data["dispatcher"]
                    state: FSMContext = dp.fsm.get_context(bot=bot, chat_id=chat.id, user_id=user.id)

                    await cmd_start(fake_message, state=state)

                    await event.callback_query.answer()

                return True

            raise