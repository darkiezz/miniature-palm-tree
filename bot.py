<<<<<<< HEAD
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from collections import deque, defaultdict

TOKEN = "8522174892:AAGaFtE1s7jNFJMJTEXr8ZxiIWdJXwAeknI"  # твой токен
ADMIN_ID = 670113559

bot = Bot(token=TOKEN)
dp = Dispatcher()

waiting_queue = deque()
pairs = {}
chat_logs = defaultdict(list)

def get_report_keyboard(reported_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оскорбления", callback_data=f"report_{reported_id}_insult")],
        [InlineKeyboardButton(text="Спам", callback_data=f"report_{reported_id}_spam")],
        [InlineKeyboardButton(text="18+/Порно", callback_data=f"report_{reported_id}_porn")],
        [InlineKeyboardButton(text="Другое", callback_data=f"report_{reported_id}_other")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать!\n\n/search — найти собеседника\n/stop — выйти из чата")

@dp.message(Command("search", "next"))
async def search_partner(message: types.Message):
    user_id = message.from_user.id
    if user_id in pairs:
        await message.answer("Ты уже в чате!")
        return
    await message.answer("🔍 **Поиск собеседника...**")
    if waiting_queue:
        partner = waiting_queue.popleft()
        pairs[user_id] = partner
        pairs[partner] = user_id
        await bot.send_message(user_id, "✅ **Партнёр найден!** Пиши.")
        await bot.send_message(partner, "✅ **Партнёр найден!** Пиши.")
    else:
        waiting_queue.append(user_id)

@dp.message(Command("stop"))
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in pairs:
        partner = pairs.pop(user_id)
        pairs.pop(partner, None)
        await bot.send_message(partner, "😔 Собеседник вышел.", reply_markup=get_report_keyboard(user_id))
        await message.answer("Чат остановлен.", reply_markup=get_report_keyboard(partner))
    elif user_id in list(waiting_queue):
        waiting_queue.remove(user_id)
        await message.answer("Вышел из очереди.")

@dp.message()
async def relay_and_log(message: types.Message):
    user_id = message.from_user.id
    if user_id not in pairs:
        return
    partner_id = pairs[user_id]
    text = message.text or "[Медиа]"
    chat_logs[user_id].append(f"Ты: {text}")
    chat_logs[partner_id].append(f"Собеседник: {text}")
    if len(chat_logs[user_id]) > 5:
        chat_logs[user_id] = chat_logs[user_id][-5:]
    await bot.copy_message(partner_id, message.chat.id, message.message_id)

@dp.callback_query(lambda c: c.data.startswith("report_"))
async def handle_report(callback: CallbackQuery):
    _, reported_id_str, reason = callback.data.split("_")
    reported_id = int(reported_id_str)
    reporter = callback.from_user.id
    log1 = "\n".join(chat_logs.get(reporter, ["Нет логов"]))
    log2 = "\n".join(chat_logs.get(reported_id, ["Нет логов"]))
    report_text = f"🚨 ЖАЛОБА!\nОт: {reporter}\nНа: {reported_id}\nПричина: {reason}\n\n=== Логи от жалобщика ===\n{log1}\n\n=== Логи от обвиняемого ===\n{log2}"
    await bot.send_message(ADMIN_ID, report_text)
    await callback.answer("Жалоба отправлена.")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("🛠 Админ-панель открыта.")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
=======
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from collections import deque, defaultdict

TOKEN = "8522174892:AAGaFtE1s7jNFJMJTEXr8ZxiIWdJXwAeknI"  # твой токен
ADMIN_ID = 670113559

bot = Bot(token=TOKEN)
dp = Dispatcher()

waiting_queue = deque()
pairs = {}
chat_logs = defaultdict(list)

def get_report_keyboard(reported_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оскорбления", callback_data=f"report_{reported_id}_insult")],
        [InlineKeyboardButton(text="Спам", callback_data=f"report_{reported_id}_spam")],
        [InlineKeyboardButton(text="18+/Порно", callback_data=f"report_{reported_id}_porn")],
        [InlineKeyboardButton(text="Другое", callback_data=f"report_{reported_id}_other")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать!\n\n/search — найти собеседника\n/stop — выйти из чата")

@dp.message(Command("search", "next"))
async def search_partner(message: types.Message):
    user_id = message.from_user.id
    if user_id in pairs:
        await message.answer("Ты уже в чате!")
        return
    await message.answer("🔍 **Поиск собеседника...**")
    if waiting_queue:
        partner = waiting_queue.popleft()
        pairs[user_id] = partner
        pairs[partner] = user_id
        await bot.send_message(user_id, "✅ **Партнёр найден!** Пиши.")
        await bot.send_message(partner, "✅ **Партнёр найден!** Пиши.")
    else:
        waiting_queue.append(user_id)

@dp.message(Command("stop"))
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in pairs:
        partner = pairs.pop(user_id)
        pairs.pop(partner, None)
        await bot.send_message(partner, "😔 Собеседник вышел.", reply_markup=get_report_keyboard(user_id))
        await message.answer("Чат остановлен.", reply_markup=get_report_keyboard(partner))
    elif user_id in list(waiting_queue):
        waiting_queue.remove(user_id)
        await message.answer("Вышел из очереди.")

@dp.message()
async def relay_and_log(message: types.Message):
    user_id = message.from_user.id
    if user_id not in pairs:
        return
    partner_id = pairs[user_id]
    text = message.text or "[Медиа]"
    chat_logs[user_id].append(f"Ты: {text}")
    chat_logs[partner_id].append(f"Собеседник: {text}")
    if len(chat_logs[user_id]) > 5:
        chat_logs[user_id] = chat_logs[user_id][-5:]
    await bot.copy_message(partner_id, message.chat.id, message.message_id)

@dp.callback_query(lambda c: c.data.startswith("report_"))
async def handle_report(callback: CallbackQuery):
    _, reported_id_str, reason = callback.data.split("_")
    reported_id = int(reported_id_str)
    reporter = callback.from_user.id
    log1 = "\n".join(chat_logs.get(reporter, ["Нет логов"]))
    log2 = "\n".join(chat_logs.get(reported_id, ["Нет логов"]))
    report_text = f"🚨 ЖАЛОБА!\nОт: {reporter}\nНа: {reported_id}\nПричина: {reason}\n\n=== Логи от жалобщика ===\n{log1}\n\n=== Логи от обвиняемого ===\n{log2}"
    await bot.send_message(ADMIN_ID, report_text)
    await callback.answer("Жалоба отправлена.")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("🛠 Админ-панель открыта.")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
9189f54b3c7e074afbba0d186baca08db80f09c5
    asyncio.run(main())