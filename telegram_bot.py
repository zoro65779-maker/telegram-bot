from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8285582675:AAEzWrdHGpEuchhT_G5njDiSJR1OdCmqf1Y"

QUESTIONS = [
    {
        "question": "What are your opinion about AI?",
        "options": ["Good", "Bad", "Neutral"],
        "answer": "Good"
    },
    {
        "question": "what are your opinion about onine money?",
        "options": ["good", "bad", "neutral"],
        "answer": "good"
    },
    {
        "question": "What are your opinion about corruption?",
        "options": ["good", "bad", "neutral"],
        "answer": "bad"
    }
]

PASS_MARK = 1
SECRET_LINK = "https://signal.group/#CjQKILua-f0KWDs0PTTDLqvO0fJyiBacucmo_5TVaLJmoCBUEhDS8sKUUzEE_73tzrtv9_ax"

# user_id → state
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "index": 0,
        "score": 0
    }
    await send_question(update, user_id)


async def send_question(update, user_id):
    q = QUESTIONS[user_data[user_id]["index"]]
    keyboard = ReplyKeyboardMarkup(
        [[opt] for opt in q["options"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(q["question"], reply_markup=keyboard)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        await update.message.reply_text("Type /start to begin.")
        return

    current_q = QUESTIONS[user_data[user_id]["index"]]

    if text == current_q["answer"]:
        user_data[user_id]["score"] += 1

    user_data[user_id]["index"] += 1

    # More questions left
    if user_data[user_id]["index"] < len(QUESTIONS):
        await send_question(update, user_id)
    else:
        # Quiz finished
        score = user_data[user_id]["score"]

        if score >= PASS_MARK:
            await update.message.reply_text(
                f"✅ Eligible!\nYour score: {score}\nAccess link:\n{SECRET_LINK}"
            )
        else:
            await update.message.reply_text(
                f"❌ You are not eligible.\nYour score: {score}"
            )

        del user_data[user_id]


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
