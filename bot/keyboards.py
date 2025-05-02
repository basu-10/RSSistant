from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.rss import valid_feeds

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Browse Categories", callback_data="categories"),
         InlineKeyboardButton("🔍 Filter Feeds", callback_data="filter")],
        [InlineKeyboardButton("🚫 Clear Filter", callback_data="clear_filter")]
    ])

def get_categories_keyboard():
    rows = []
    row = []
    for i, cat in enumerate(valid_feeds):
        row.append(InlineKeyboardButton(cat.capitalize().replace("_", " "), callback_data=f"category:{cat}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("🏠 Back to Main Menu", callback_data="start")])
    return InlineKeyboardMarkup(rows)

def get_feeds_keyboard(category):
    entries = valid_feeds.get(category, [])
    buttons = []
    for i in range(0, len(entries), 2):
        row = []
        for j in range(2):
            if i + j < len(entries):
                entry = entries[i + j]
                row.append(InlineKeyboardButton(entry.get("Title", "Untitled"), callback_data=f"feed:{category}:{i + j}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="categories")])
    return InlineKeyboardMarkup(buttons)

def get_post_article_nav(category):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Feeds", callback_data=f"category:{category}"),
         InlineKeyboardButton("🗂️ Show Categories", callback_data="categories")]
    ])
