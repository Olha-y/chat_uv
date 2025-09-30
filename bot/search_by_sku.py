from telegram import Update
from telegram.ext import ContextTypes
from app.models import repo, Product
from product_actions import show_product, send_photos, send_pdf


async def handle_sku_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    query = update.message.text.strip()

    if not query.isdigit():
        await update.message.reply_text(
            "❌ Please enter a valid SKU. Use numeric input from 0-9."
        )
        return

    await update.message.reply_text(f"🔍 SEARCH by SKU: {query}")

    products = await repo.find_by(
        {"sku": {"$regex": f"(^|\\|){query}($|\\|)", "$options": "i"}}
    )

    if not products:
        await update.message.reply_text(
            "❌ Product not found. Try another SKU...\n\n"
            "<i>To return to the beginning, click /start</i>",
    parse_mode="HTML"
        )
        return

    product = products[0]
    if isinstance(product, dict):
        product = Product(**product)
    context.user_data["current_product"] = product

    await show_product(update, product, prefix="sku")
    await update.message.reply_text(
        "<i>To return to the beginning, click /start</i>",
        parse_mode="HTML"
    )


async def sku_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    product = context.user_data.get("current_product")

    if not product:
        await query.answer("⚠️ Product not found.", show_alert=True)
        return

    if data.startswith("sku_photos_"):
        await send_photos(update, context, product)
    elif data.startswith("sku_pdf_"):
        await send_pdf(update, context, product)

