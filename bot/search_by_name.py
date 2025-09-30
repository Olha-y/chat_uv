from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.models import repo, Product
from product_actions import show_product, send_photos, send_pdf



PAGE_SIZE = 2


async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    query = update.message.text.strip()

    if not query or len(query) < 2:
        await update.message.reply_text("❌ Enter at least 2 characters.")
        return

    await update.message.reply_text(f"📖 Search by name: {query}")

    products = await repo.find_by({"name": {"$regex": query, "$options": "i"}})

    if not products:
        await update.message.reply_text("❌ No products found.")
        return


    context.user_data["search_results"] = [p.dict() for p in products]
    context.user_data["page"] = 0

    await show_products_page(update, context)
    await update.message.reply_text("<i>To return to the beginning, click /start</i>", parse_mode="HTML")


async def show_products_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = context.user_data.get("search_results", [])
    page = context.user_data.get("page", 0)

    if not results:
        await update.message.reply_text("❌ No results to display.\n\n<i>To return to the beginning, click /start</i>",
    parse_mode="HTML")
        return

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = results[start:end]

    keyboard = []
    for idx, product_data in enumerate(page_items):
        product = Product(**product_data)
        keyboard.append(
            [InlineKeyboardButton(f"📦 {product.name}", callback_data=f"name_select_{start + idx}")]
        )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ BACK", callback_data="name_page_prev"))
    if end < len(results):
        nav_buttons.append(InlineKeyboardButton("➡️ NEXT", callback_data="name_page_next"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            f"📑 RESULTS {start+1}–{min(end, len(results))} з {len(results)}:",
            reply_markup=reply_markup,
        )
    else:
        await update.callback_query.edit_message_text(
            f"📑 RESULTS {start+1}–{min(end, len(results))} з {len(results)}:",
            reply_markup=reply_markup,
        )


async def name_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    results = context.user_data.get("search_results", [])
    page = context.user_data.get("page", 0)

    if data == "name_page_prev":
        context.user_data["page"] = max(0, page - 1)
        await show_products_page(update, context)
    elif data == "name_page_next":
        context.user_data["page"] = page + 1
        await show_products_page(update, context)
    elif data.startswith("name_select_"):
        index = int(data.replace("name_select_", ""))
        if 0 <= index < len(results):
            product = Product(**results[index])
            context.user_data["current_product"] = product
            await show_product(query, product, prefix="name")
    elif data.startswith("name_photos_"):
        product = context.user_data.get("current_product")
        if product:
            await send_photos(update, context, product)
    elif data.startswith("name_pdf_"):
        product = context.user_data.get("current_product")
        if product:
            await send_pdf(update, context, product)
