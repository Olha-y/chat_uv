from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os


load_dotenv()



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(user_message)


if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN not in в .env file!")


    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()
