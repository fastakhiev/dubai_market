from aiogram import Router
from aiogram.types import Update, Message
from aiogram.exceptions import TelegramBadRequest
from app.handlers.v1.sign_up import cmd_start
from app.core.bot import bot

router = Router()

@router.errors()
async def global_error_handler(update: Update, exception: Exception):
    if isinstance(exception, TelegramBadRequest):
        error_text = str(exception)

        if "message can't be edited" in error_text or "message to edit not found" in error_text or "message can't be deleted" in error_text:
            if update.callback_query:
                user = update.callback_query.from_user
                chat = update.callback_query.message.chat
                message_id = update.callback_query.message.message_id

                fake_message = Message(
                    message_id=message_id,
                    date=update.callback_query.message.date,
                    chat=chat,
                    from_user=user,
                    text="/start",
                    message_thread_id=None
                )

                state = await router.fsm.get_context(bot, chat.id, user.id)

                await cmd_start(fake_message, state=state)

            return True

    return False