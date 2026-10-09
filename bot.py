import logging
import os
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# --- Configuration (Loaded from Environment Variables) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001234567890")) 

WELCOME_MESSAGE = """
Welcome to the channel! 🎉

To get started, please read the pinned message and follow the rules.

If you have any questions, feel free to ask.
"""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    join_request = update.chat_join_request
    user_id = join_request.from_user.id

    try:
        # Send the welcome message privately to the user
        await context.bot.send_message(chat_id=user_id, text=WELCOME_MESSAGE)
        logger.info(f"Sent welcome message to user {user_id}")

        # Automatically approve the join request
        await join_request.approve()
        logger.info(f"Approved join request for user {user_id}")

    except Exception as e:
        logger.error(f"Error processing join request for user {user_id}: {e}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(ChatJoinRequestHandler(handle_join_request, chat_id=CHANNEL_ID))
    
    logger.info("Bot is starting as a background worker...")
    application.run_polling()

if __name__ == "__main__":
    main()
