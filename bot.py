import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# --- Configuration (Loaded from Environment Variables) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ---> YOUR CHANNEL ID <---
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003757455410")) 

# ---> YOUR DIRECT IMAGE URL <---
IMAGE_URL = "https://i.imgur.com/7aslkfT.jpeg"

# The new welcome message
WELCOME_MESSAGE = """There are many large orders—grab them now! 🔥🔥🔥 The selling super fast 🔤🔤

OFFICIAL LINK : https://wallet.paisa-base.com/register?inviteCode=phar6p

🔤🔤 Please check your account balance first. If there is a balance but no sales, check your UPI tools. 

🛍Don’t always wait to sell your entire balance before buying. Once the token drops below 🤩🤩🤩🤩  Rupees, please buy it immediately! Keep it above 🤩🤩🤩🤩  Rupees and always to sell quickly!🏷🏷🏷

👑Contact :@jetlee261"""

# --- Enable logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Handler for Chat Join Requests ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with an image to the user when they request to join."""
    join_request = update.chat_join_request
    user_id = join_request.from_user.id

    try:
        # Send the welcome message with the image
        await context.bot.send_photo(
            chat_id=user_id,
            photo=IMAGE_URL,
            caption=WELCOME_MESSAGE
        )
        logger.info(f"Sent welcome message with image to user {user_id}")

        # Automatically approve the join request
        await join_request.approve()
        logger.info(f"Approved join request for user {user_id}")

    except Exception as e:
        logger.error(f"Error processing join request for user {user_id}: {e}")

def main() -> None:
    """Start the bot."""
    
    # --- Python 3.12+ Event Loop Workaround ---
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # ------------------------------------------

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(ChatJoinRequestHandler(handle_join_request, chat_id=CHANNEL_ID))

    logger.info("Bot is starting as a background worker...")
    application.run_polling()

if __name__ == "__main__":
    main()
