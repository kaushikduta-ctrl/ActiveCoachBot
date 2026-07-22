import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.environ.get("BOT_TOKEN")  # Railway will set this
if not TOKEN:
    raise ValueError("No BOT_TOKEN found! Set it in Railway environment variables.")

# Enable logging (good for debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- SAFE, MODERATION-FRIENDLY CONTENT ---
# No superlatives, no gambling, no income promises.
WORKOUTS = [
    "🏋️ **Push-ups**: 3 sets of 12 reps. Keep your back straight!",
    "🦵 **Squats**: 3 sets of 15 reps. Go as low as comfortable.",
    "🏃 **Jumping Jacks**: 3 sets of 30 seconds. Great for warm-up.",
    "💪 **Plank**: Hold for 45 seconds. 3 sets. Engage your core.",
    "🧘 **Lunges**: 3 sets of 10 per leg. Step forward, not sideways.",
]

TIPS = [
    "💧 Drink water before, during, and after your workout.",
    "😴 Sleep 7-9 hours – that's when your muscles recover.",
    "🥗 Eat protein within 1 hour after training for best results.",
    "📈 Track your progress weekly, not daily. Consistency beats intensity.",
    "🧘 Stretch for 5 minutes after every session to prevent injury.",
]

# --- BOT COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message - clear, friendly, and descriptive."""
    await update.message.reply_text(
        "🏋️ Welcome to Active4CoachBot!\n\n"
        "I'm your personal fitness guide on Telegram. "
        "I give you safe, effective workout ideas and tips to stay active.\n\n"
        "📌 **Commands:**\n"
        "/workout – Get a random exercise\n"
        "/tip – Receive a fitness tip\n"
        "/help – See this message again\n\n"
        "💡 No gimmicks – just real, useful guidance."
    )

async def workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random workout suggestion."""
    choice = random.choice(WORKOUTS)
    await update.message.reply_text(choice)

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fitness tip."""
    choice = random.choice(TIPS)
    await update.message.reply_text(choice)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command - repeats the start message."""
    await start(update, context)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fallback for unrecognized commands."""
    await update.message.reply_text(
        "❓ I don't recognize that command. Type /help to see available commands."
    )

# --- MAIN FUNCTION ---

def main():
    """Start the bot."""
    # Create the Application
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("workout", workout))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("unknown", unknown))  # Fallback

    # Start polling
    logger.info("✅ Active4CoachBot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
