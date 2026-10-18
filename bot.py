import logging
import os
import asyncio
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# --- Configuration (Loaded from Environment Variables) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003757455410")) 

# ---> YOUR DIRECT IMAGE URLS <---
IMAGE_URL_1 = "https://i.imgur.com/MxL0p5j.jpeg"
IMAGE_URL_2 = "https://i.imgur.com/nuoMW89.jpeg"

# The new welcome message
WELCOME_MESSAGE = """📌💰New Long Term Application Launch Today 📈

☄️Best Earning App Long Term📌
✅App Name : 🚩🚩   🚩🚩🚩
✅ Launched Date: 9 oct 💠 

📌🔤🔤🔤🔤🔤🔤🔤🔤
👆Invest ₹280/- Daily ₹240🛫
👆Invest ₹2800/- Daily ₹2436🎉

📌Daily plan 🔤🔤🔤🔤
👆Invest ₹500, Next Day Get 1000
👆Invest ₹1000, Next Day Get ₹4000

✅ App Registration Link:  ⬇️⬇️

https://www.heavymachinery9.ru/?invitation_code=F7852
https://www.heavymachinery9.ru/?invitation_code=F7852

👑సభ్యులారా, ఈ యాప్‌ను అస్సలు మిస్ అవ్వకండి. ఇది 2 నెలలకు పైగా అందుబాటులో ఉంటుంది. ✅
🎖️ ప్రతి చెల్లుబాటు అయ్యే సభ్యునికి స్పిన్ చేసే అవకాశం లభిస్తుంది. ✔️

✅ ఈ యాప్ 50-60 రోజుల పాటు అందుబాటులో ఉంటుంది. ప్రతి ఒక్కరూ తమ సొంత బృందాన్ని ఏర్పాటు చేసుకుని ఇందులో పాల్గొనవచ్చు. 💘"""

# --- Enable logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Handler for Chat Join Requests ---
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an album with the welcome message when they request to join."""
    join_request = update.chat_join_request
    user_id = join_request.from_user.id

    try:
        # Prepare the media group (album)
        media_group = [
            InputMediaPhoto(media=IMAGE_URL_1, caption=WELCOME_MESSAGE),
            InputMediaPhoto(media=IMAGE_URL_2)
        ]

        # Send the album with the welcome message
        await context.bot.send_media_group(chat_id=user_id, media=media_group)
        logger.info(f"Sent welcome album to user {user_id}")

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
