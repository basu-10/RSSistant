import logging

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error("Exception:", exc_info=context.error)
    try:
        if update.message:
            await update.message.reply_text("⚠️ An error occurred while handling your message.")
        elif update.callback_query:
            await update.callback_query.message.reply_text("⚠️ Error with button interaction.")
    except Exception:
        pass
