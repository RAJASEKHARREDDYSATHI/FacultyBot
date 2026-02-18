from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from data_loader import load_data
import os

TOKEN = os.getenv("BOT_TOKEN")



faculty_data = load_data()

# 🔹 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Faculty Finder Bot\n\n"
        "🔎 Send faculty name to get details\n"
        "Example: radhika"
    )

# 🔹 Search Function
def search_faculty(query):
    query = query.lower().strip()
    results = []

    for key, value in faculty_data.items():
        if query in key:
            results.append(value)

    return results

# 🔹 Format Response
def format_response(results):
    text = ""

    for i, data in enumerate(results[:5], 1):
        text += f"""👨‍🏫 {i}. {data['name']}
🏢 Dept: {data['dept']}
📍 Room: {data['room']}

"""

    return text

# 🔹 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    results = search_faculty(user_input)

    if not results:
        await update.message.reply_text(
            "❌ Faculty not found\n\nTry again with correct name."
        )
        return

    reply = format_response(results)

    await update.message.reply_text(reply)

# 🔹 Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 How to use:\n"
        "- Send faculty name\n"
        "- Example: 'radhika'\n\n"
        "Bot will return department & cabin number"
    )

# 🔹 Main Function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
