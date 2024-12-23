from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from hellman import hellman
from adleman import adleman
from adleman2 import adleman
import asyncio

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("взаимодействие с решалкой:\n\n/hellman g a n\n/adleman g a n\n/polinom дима лох")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ты сказал: {update.message.text}")

async def hellman_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        g, a, n = map(int, context.args)

        async def run_hellman():
            result, detailed_solution = hellman(g, a, n)
            return detailed_solution

        detailed_solution = await asyncio.wait_for(run_hellman(), timeout=10.0)

        await update.message.reply_text(f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2")

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def adleman_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        g, a, n = map(int, context.args)

        async def run_hellman():
            result, detailed_solution = adleman(g, a, n)
            return detailed_solution

        detailed_solution = await asyncio.wait_for(run_hellman(), timeout=10.0)

        await update.message.reply_text(f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2")

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def adleman2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        g, a, n = map(int, context.args)

        async def run_hellman():
            result, detailed_solution = adleman2(g, a, n)
            return detailed_solution

        detailed_solution = await asyncio.wait_for(run_hellman(), timeout=10.0)

        await update.message.reply_text(f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2")

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hellman", hellman_command))
    application.add_handler(CommandHandler("adleman", adleman_command))
    application.add_handler(CommandHandler("adleman2", adleman2_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == "__main__":
    main()
