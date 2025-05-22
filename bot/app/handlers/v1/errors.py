from aiogram import Router
from aiogram.types import Update, Message
from aiogram.exceptions import TelegramBadRequest
from app.handlers.v1.sign_up import cmd_start
from app.core.bot import bot

router = Router()

@router.error()
async def global_error_handler(event: Update, exception: Exception) -> bool:
    if isinstance(exception, TelegramBadRequest):
        error_text = str(exception)

        if "message can't be edited" in error_text or "message to edit not found" in error_text or "message can't be deleted for everyone" in error_text:
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
                )

                state = await router.fsm.get_context(bot, chat.id, user.id)
                await cmd_start(fake_message, state=state)

            return True

    return False