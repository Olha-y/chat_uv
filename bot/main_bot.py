import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from search_by_sku import handle_sku_input, sku_button_handler
from search_by_name import handle_name_input, name_button_handler


logging.basicConfig(level=logging.INFO)
load_dotenv()
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔗 <b>Link to {name_site} site:</b>\n"
        "• <a href='#'>{name_site}</a>\n\n"
    
        "🔍 <b>SEARCHING GOODS:</b>\n"
        "Choose a search method below 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🔍 Search by SKU", callback_data="search_sku")],
        [InlineKeyboardButton("📖 Search by name", callback_data="search_name")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


async def block_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and not update.message.text:
        await update.message.reply_text(
            "⚠️ Please use only text and buttons.."
        )
        return


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query


    if query.data == "search_sku":
        context.user_data["mode"] = "sku"
        await query.message.reply_text(
            "🔍*ENTER THE SKU*:",
            parse_mode="Markdown"
        )

    elif query.data == "search_name":
        context.user_data["mode"] = "name"
        await query.message.reply_text(
            "📖 *ENTER THE PRODUCT NAME*:",
            parse_mode="Markdown"
        )


async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")

    if mode == "sku":
        await handle_sku_input(update, context)
    elif mode == "name":
        await handle_name_input(update, context)
    else:
        await update.message.reply_text(
            "⚠️ First, choose a search method via /start."
        )


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN not found in environment variables")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_handler, pattern="^(search_)"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    application.add_handler(CallbackQueryHandler(sku_button_handler, pattern="^sku_"))
    application.add_handler(CallbackQueryHandler(name_button_handler, pattern="^name_"))
    application.add_handler(MessageHandler(~filters.TEXT, block_non_text), group=0)


    print("✅ Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
