import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# --- Configuration (Loaded from Environment Variables) ---
# Make sure you set these in your Render Dashboard under "Environment"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001234567890")) 

# The message to send to users when they request to join
WELCOME_MESSAGE = """
Welcome to the channel! 🎉

To get started, please read the pinned message and follow the rules.

If you have any questions, feel free to ask.
"""

# --- Enable logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Handler for Chat Join Requests ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to the user when they request to join the channel."""
    join_request = update.chat_join_request
    user_id = join_request.from_user.id

    try:
        # Send the welcome message privately to the user
        await context.bot.send_message(chat_id=user_id, text=WELCOME_MESSAGE)
        logger.info(f"Sent welcome message to user {user_id}")

        # Optional: Automatically approve the join request
        # If you want to manually approve users, comment out the next line
        await join_request.approve()
        logger.info(f"Approved join request for user {user_id}")

    except Exception as e:
        logger.error(f"Error processing join request for user {user_id}: {e}")

def main() -> None:
    """Start the bot."""
    
    # --- Python 3.12+ Event Loop Workaround ---
    # Render uses Python 3.14 which requires an explicitly set event loop.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # ------------------------------------------

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the handler for chat join requests
    application.add_handler(ChatJoinRequestHandler(handle_join_request, chat_id=CHANNEL_ID))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is starting as a background worker...")
    application.run_polling()

if __name__ == "__main__":
    main()
