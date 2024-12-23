from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from hellman import hellman
from adleman import adleman
from adleman2 import adleman2
from SF import solve_polynomial
from factor import factor
import asyncio

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("взаимодействие с решалкой:\n\n/hellman g a n\n/adleman g a n\n/adleman2 g a n (он дополнительно расипсывает систему, но иногда криво, так что если криво, то первый вариант)\n/factor c0 c1 c2 ... cN p\n\n/SF c0 c1 c2 ... cN p (это для отладки сделано)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ты написал какую-то хуйню, перепроверь:\n{update.message.text}")

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

# Обработчик команды /factor
async def factor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /factor для факторизации полинома.
    
    Формат команды:
    /factor c0 c1 c2 ... cN p
    
    Где:
    - c0, c1, ..., cN: Коэффициенты полинома от старшей к младшей степени.
    - p: Модуль p для поля Z_p.
    
    Пример:
    /factor 1 0 1 0 1 1 2
    """
    try:
        # Проверяем, что передано как минимум два аргумента (коэффициенты и p)
        if len(context.args) < 2:
            await update.message.reply_text(
                "Ошибка: Требуется как минимум два аргумента.\n"
                "Формат: /factor c0 c1 c2 ... cN p\n"
                "Пример: /factor 1 0 1 0 1 1 2"
            )
            return

        # Последний аргумент — p, остальные — коэффициенты
        *coeffs_str, p_str = context.args

        # Преобразуем коэффициенты и p в целые числа
        coeffs = list(map(int, coeffs_str))
        p = int(p_str)

        # Запускаем вычисление в отдельном потоке, чтобы не блокировать основной поток
        loop = asyncio.get_event_loop()
        detailed_solution = await loop.run_in_executor(
            None, factor, coeffs, p
        )

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /factor c0 c1 c2 ... cN p\n"
            "Пример: /factor 1 0 1 0 1 1 2"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def SF_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /SF для разложения полинома на свободные квадраты.

    Формат команды:
    /SF c0 c1 c2 ... cN p

    Где:
    - c0, c1, ..., cN: Коэффициенты полинома от старшей к младшей степени.
    - p: Модуль p для поля Z_p.

    Пример:
    /SF 1 0 2 0 1 1 3
    """
    try:
        # Проверяем, что передано как минимум два аргумента (коэффициенты и p)
        if len(context.args) < 2:
            await update.message.reply_text(
                "Ошибка: Требуется как минимум два аргумента.\n"
                "Формат: /SF c0 c1 c2 ... cN p\n"
                "Пример: /SF 1 0 2 0 1 1 3"
            )
            return

        # Последний аргумент — p, остальные — коэффициенты
        *coeffs_str, p_str = context.args

        # Преобразуем коэффициенты и p в целые числа
        coeffs = list(map(int, coeffs_str))
        p = int(p_str)

        # Запускаем вычисление в отдельном потоке, чтобы не блокировать основной поток
        loop = asyncio.get_event_loop()
        detailed_solution = await loop.run_in_executor(
            None, solve_polynomial, coeffs, p
        )

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /SF c0 c1 c2 ... cN p\n"
            "Пример: /SF 1 0 2 0 1 1 3"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hellman", hellman_command))
    application.add_handler(CommandHandler("adleman", adleman_command))
    application.add_handler(CommandHandler("adleman2", adleman2_command))
    application.add_handler(CommandHandler("factor", factor_command))
    application.add_handler(CommandHandler("SF", SF_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == "__main__":
    main()
