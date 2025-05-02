from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import get_main_menu_keyboard, get_categories_keyboard, get_feeds_keyboard, get_post_article_nav
from bot.filters import user_filters, save_user_filters
from bot.rss import valid_feeds, fetch_rss_feed

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=get_main_menu_keyboard())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    data = query.data

    if data == "categories":
        await query.message.reply_text("📂 Choose a category:", reply_markup=get_categories_keyboard())

    elif data == "filter":
        existing = user_filters.get(user_id)
        msg = f"🔎 Current filter: {', '.join(existing)}" if existing else "🔎 No filter set."
        context.user_data["awaiting_filter"] = True
        await query.message.reply_text(
            f"{msg}\n\n✏️ Enter new keywords, comma-separated. This will overwrite current filter.\n⛔️ Use /start to exit."
        )

    elif data == "clear_filter":
        user_filters.pop(user_id, None)
        save_user_filters(user_filters)
        await query.message.reply_text("✅ Filter cleared.", reply_markup=get_main_menu_keyboard())

    elif data.startswith("category:"):
        category = data.split(":", 1)[1]
        if category not in valid_feeds:
            await query.message.reply_text("⚠️ Category not found.")
        else:
            await query.message.reply_text(
                f"📄 Choose a feed under *{category}*:", reply_markup=get_feeds_keyboard(category), parse_mode='Markdown'
            )

    elif data.startswith("feed:"):
        _, category, idx = data.split(":")
        idx = int(idx)
        feeds = valid_feeds.get(category, [])
        if idx >= len(feeds):
            await query.message.reply_text("⚠️ Feed not found.")
            return
        feed_entry = feeds[idx]
        feed_url = feed_entry["RSS Feed Url"]
        feed_title = feed_entry["Title"]
        rss_data = fetch_rss_feed(feed_url)

        if not rss_data or not rss_data.entries:
            await query.message.reply_text(f"⚠️ Could not load: {feed_title}")
            return

        # Apply filters
        filters_list = user_filters.get(user_id, [])
        filtered = [
            entry for entry in rss_data.entries
            if not filters_list or any(word.lower() in f"{entry.title} {entry.get('description', '')}".lower()
                                       for word in filters_list)
        ]

        if not filtered:
            await query.message.reply_text(f"📭 No articles matched your filter in '{feed_title}'. Clear filter to get ALL results...")
            return

        for i in range(0, len(filtered), 5):
            chunk = filtered[i:i+5]
            text = "\n\n".join(f"{i+1}. {e.title}\n{e.link}" for i, e in enumerate(chunk))
            await query.message.reply_text(text, disable_web_page_preview=True)

        await query.message.reply_text("📌 What next?", reply_markup=get_post_article_nav(category))

    elif data == "start":
        await query.message.reply_text("🏠 Main menu:", reply_markup=get_main_menu_keyboard())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if context.user_data.get("awaiting_filter"):
        raw = update.message.text
        keywords = [k.strip().lower() for k in raw.split(",") if k.strip()]
        if not keywords:
            await update.message.reply_text("⚠️ No valid keywords found.")
        else:
            user_filters[user_id] = keywords
            save_user_filters(user_filters)
            context.user_data["awaiting_filter"] = False
            await update.message.reply_text(f"✅ Filter set: {', '.join(keywords)}", reply_markup=get_main_menu_keyboard())
    else:
        await update.message.reply_text("❓ I didn’t understand that. Use /start.")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Unknown command. Use /start")
