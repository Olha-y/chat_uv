import os
import logging
from dotenv import load_dotenv
from config import resolve_path
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes
from app.models import Product
from file_utils import process_image


load_dotenv()


async def show_product(update, product: Product, prefix: str):
    keyboard = [
        [InlineKeyboardButton("🖼 Photo", callback_data=f"{prefix}_photos_{product.sku}")],
        [InlineKeyboardButton("📄 PDF", callback_data=f"{prefix}_pdf_{product.sku}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"📦 <b>{product.name}</b>\n\nSKU: {product.sku}"

    if hasattr(update, "message") and update.message:
        await update.message.reply_text(
            text, parse_mode="HTML",
            reply_markup=reply_markup
        )
    elif hasattr(update, "callback_query") and update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode="HTML",
            reply_markup=reply_markup
        )


async def send_photos(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        product: Product
    ):
    """
    Sends a product photo via Telegram.
    If there are multiple photos, use send_media_group().
    """

    query = update.callback_query
    if query:
        await query.answer()
        chat_id = query.message.chat.id
    else:
        chat_id = update.effective_chat.id


    image_paths = list(getattr(product, "image_url", []))
    media_group = []

    logging.debug(f"product.image_url={product.image_url}")

    for idx, path in enumerate(image_paths):
        full_path = resolve_path(path)

        try:
            media = await process_image(full_path)
            caption = f"{product.name}" if idx == 0 else None
            media_group.append(InputMediaPhoto(media=media, caption=caption))
        except Exception as e:
            logging.exception(f"Can't process image: {full_path}: {e}")

    if not media_group:
        if query:
            await query.edit_message_text("⚠️ Photo could not be uploaded..")
        return


    if len(media_group) > 1:
        await context.bot.send_media_group(chat_id=chat_id, media=media_group)
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=media_group[0].media,
            caption=media_group[0].caption,
        )


async def send_pdf(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        product: Product
    ):
    query = update.callback_query
    await query.answer()

    pdf_path = resolve_path(product.specification_url)

    if not pdf_path or not os.path.isfile(pdf_path):
        await query.edit_message_text("⚠️ PDF - file not found.")
        return

    try:
        with open(pdf_path, "rb") as f:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=f,
                filename=os.path.basename(pdf_path),
                caption=f"📄 Specification for {product.name}",
            )
    except Exception as e:
        logging.warning(f"Failed to send PDF {pdf_path}: {e}")
        await query.edit_message_text(
            "⚠️ An error occurred while sending PDF."
        )
