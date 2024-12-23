# bot.py

import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import os
from hellman import hellman
from adleman import adleman
from adleman2 import adleman2
from SF import solve_polynomial
from factor import factor
from gcd import gcd_polynomials  # Импортируем функцию gcd_polynomials
from typing import List

# Загрузка переменных окружения из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def is_prime(n: int) -> bool:
    """
    Проверяет, является ли число простым.
    
    :param n: Число для проверки.
    :return: True, если число простое, иначе False.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Взаимодействие с решалкой:\n\n"
        "/hellman g a n - Выполнить алгоритм Хеллмана\n"
        "/adleman g a n - Выполнить алгоритм Адлемана\n"
        "/adleman2 g a n - Выполнить модифицированный алгоритм Адлемана (он дополнительно расписывает систему, но иногда криво, так что если криво, то первый вариант)\n"
        "/factor c0 c1 ... cN p - Факторизовать полином\n"
        "/gcd c0 c1 ... cN | d0 d1 ... dM p - Вычислить НОД двух полиномов\n"
        "/SF c0 c1 ... cN p - Разложить полином на свободные квадраты (для отладки)"
    )

# Обработчик сообщений, не являющихся командами
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написал какую-то хуйню, перепроверь:\n{update.message.text}")

# Вспомогательная функция для выполнения команд с таймаутом
async def execute_with_timeout(func, *args, timeout=10.0):
    return await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(None, func, *args),
        timeout=timeout
    )

# Обработчик команды /hellman
async def hellman_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text(
                "Ошибка: Требуется три аргумента.\n"
                "Формат: /hellman g a n\n"
                "Пример: /hellman 2 5 23"
            )
            return

        g, a, n = map(int, context.args)

        # Запуск функции hellman в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(hellman, g, a, n, timeout=10.0)

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /hellman g a n\n"
            "Пример: /hellman 2 5 23"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /adleman
async def adleman_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text(
                "Ошибка: Требуется три аргумента.\n"
                "Формат: /adleman g a n\n"
                "Пример: /adleman 2 5 23"
            )
            return

        g, a, n = map(int, context.args)

        # Запуск функции adleman в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(adleman, g, a, n, timeout=10.0)

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /adleman g a n\n"
            "Пример: /adleman 2 5 23"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /adleman2
async def adleman2_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text(
                "Ошибка: Требуется три аргумента.\n"
                "Формат: /adleman2 g a n\n"
                "Пример: /adleman2 2 5 23"
            )
            return

        g, a, n = map(int, context.args)

        # Запуск функции adleman2 в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(adleman2, g, a, n, timeout=10.0)

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /adleman2 g a n\n"
            "Пример: /adleman2 2 5 23"
        )
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

        # Проверяем, что p является простым числом
        if not is_prime(p):
            await update.message.reply_text("Ошибка: Модуль p должен быть простым числом.")
            return

        # Запускаем вычисление в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(factor, coeffs, p, timeout=10.0)

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /factor c0 c1 c2 ... cN p\n"
            "Пример: /factor 1 0 1 0 1 1 2"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /SF
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

        # Проверяем, что p является простым числом
        if not is_prime(p):
            await update.message.reply_text("Ошибка: Модуль p должен быть простым числом.")
            return

        # Запускаем вычисление в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(solve_polynomial, coeffs, p, timeout=10.0)

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все аргументы должны быть целыми числами.\n"
            "Формат: /SF c0 c1 c2 ... cN p\n"
            "Пример: /SF 1 0 2 0 1 1 3"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /gcd
async def gcd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /gcd для вычисления НОД двух полиномов.
    
    Формат команды:
    /gcd c0 c1 c2 ... cN | d0 d1 ... dM p
    
    Где:
    - c0, c1, ..., cN: Коэффициенты первого полинома от старшей к младшей степени.
    - d0, d1, ..., dM: Коэффициенты второго полинома от старшей к младшей степени.
    - p: Модуль p для поля Z_p.
    
    Пример:
    /gcd 1 0 1 | 1 1 0 1 2
    """
    try:
        # Объединяем все аргументы в строку
        input_str = ' '.join(context.args)
        
        # Ищем разделитель '|'
        if '|' not in input_str:
            await update.message.reply_text(
                "Ошибка: Требуется разделитель '|'.\n"
                "Формат: /gcd c0 c1 c2 ... cN | d0 d1 ... dM p\n"
                "Пример: /gcd 1 0 1 | 1 1 0 1 2"
            )
            return

        # Разделяем по '|'
        poly1_str, rest = input_str.split('|', 1)
        poly1_coeffs = list(map(int, poly1_str.strip().split()))
        
        # Разделяем rest на второй полином и p
        rest_parts = rest.strip().split()
        if len(rest_parts) < 2:
            await update.message.reply_text(
                "Ошибка: Требуется как минимум два аргумента после '|'.\n"
                "Формат: /gcd c0 c1 c2 ... cN | d0 d1 ... dM p\n"
                "Пример: /gcd 1 0 1 | 1 1 0 1 2"
            )
            return
        
        *poly2_coeffs_str, p_str = rest_parts
        poly2_coeffs = list(map(int, poly2_coeffs_str))
        p = int(p_str)

        # Проверяем, что p является простым числом
        if not is_prime(p):
            await update.message.reply_text("Ошибка: Модуль p должен быть простым числом.")
            return

        # Запускаем вычисление НОД в отдельном потоке с таймаутом 10 секунд
        detailed_solution = await execute_with_timeout(
            gcd_polynomials, poly1_coeffs, poly2_coeffs, p, timeout=10.0
        )

        # Ограничиваем длину сообщения Telegram (4096 символов)
        if len(detailed_solution) > 4000:
            detailed_solution = detailed_solution[:4000] + "\n... (сообщение слишком длинное)"

        # Отправляем ответ пользователю с использованием форматирования Markdown
        await update.message.reply_text(
            f"```\n{detailed_solution}\n```", parse_mode="MarkdownV2"
        )

    except asyncio.TimeoutError:
        await update.message.reply_text("Ошибка: Превышено время ожидания (таймаут 10 секунд).")
    except ValueError:
        await update.message.reply_text(
            "Ошибка: Все коэффициенты и p должны быть целыми числами.\n"
            "Формат: /gcd c0 c1 c2 ... cN | d0 d1 ... dM p\n"
            "Пример: /gcd 1 0 1 | 1 1 0 1 2"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Основная функция для запуска бота
def main():
    # Создаем приложение бота
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hellman", hellman_command))
    application.add_handler(CommandHandler("adleman", adleman_command))
    application.add_handler(CommandHandler("adleman2", adleman2_command))
    application.add_handler(CommandHandler("factor", factor_command))
    application.add_handler(CommandHandler("gcd", gcd_command))  # Добавляем обработчик /gcd
    application.add_handler(CommandHandler("SF", SF_command))

    # Добавляем обработчик для текстовых сообщений, не являющихся командами
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
