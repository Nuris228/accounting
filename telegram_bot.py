import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from datetime import datetime
import requests  # Для запросов к вашему FastAPI

# Конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8000"  # URL вашего FastAPI-сервера

# Клавиатура для быстрого выбора
KEYBOARD = ReplyKeyboardMarkup(
    [["/add_income", "/add_expense"], ["/report"]], resize_keyboard=True
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Добро пожаловать в бота для учета финансов!\n"
        "Используйте команды:\n"
        "/add_income [сумма] [категория] - добавить доход\n"
        "/add_expense [сумма] [категория] - добавить расход\n"
        "/report - получить отчет",
        reply_markup=KEYBOARD,
    )

# Добавление дохода
async def add_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount, category = context.args[0], " ".join(context.args[1:])
        transaction = {
            "amount": float(amount),
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": "income",
        }
        response = requests.post(f"{API_URL}/transactions/", json=transaction)
        await update.message.reply_text(f"✅ Доход {amount} ₽ добавлен!")
    except Exception as e:
        await update.message.reply_text("🚫 Ошибка. Пример: /add_income 5000 Зарплата")

# Добавление расхода
async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount, category = context.args[0], " ".join(context.args[1:])
        transaction = {
            "amount": float(amount),
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": "expense",
        }
        response = requests.post(f"{API_URL}/transactions/", json=transaction)
        await update.message.reply_text(f"✅ Расход {amount} ₽ добавлен!")
    except Exception as e:
        await update.message.reply_text("🚫 Ошибка. Пример: /add_expense 300 Еда")

# Получение отчета
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f"{API_URL}/transactions/")
    transactions = response.json()
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense

    report_text = (
        f"📊 Отчет:\n"
        f"Доходы: {total_income} ₽\n"
        f"Расходы: {total_expense} ₽\n"
        f"Баланс: {balance} ₽"
    )
    await update.message.reply_text(report_text)

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_income", add_income))
    app.add_handler(CommandHandler("add_expense", add_expense))
    app.add_handler(CommandHandler("report", report))
    app.run_polling()

if __name__ == "__main__":
    main()