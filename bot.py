import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from collections import deque, defaultdict

TOKEN = "8522174892:AAGaFtE1s7jNFJMJTEXr8ZxiIWdJXwAeknI"
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
    await message.answer("👋 Добро пожаловать в анонимный чат!\n/search — найти собеседника")

@dp.message(Command("search", "next"))
async def search_partner(message: types.Message):
    user_id = message.from_user.id
    if user_id in pairs:
        await message.answer("Ты уже в чате!")
        return
    await message.answer("🔍 Поиск собеседника...")
    if waiting_queue:
        partner = waiting_queue.popleft()
        pairs[user_id] = partner
        pairs[partner] = user_id
        await bot.send_message(user_id, "✅ Партнёр найден!")
        await bot.send_message(partner, "✅ Партнёр найден!")
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

@dp.message()
async def relay(message: types.Message):
    user_id = message.from_user.id
    if user_id not in pairs:
        return
    partner_id = pairs[user_id]
    await bot.copy_message(partner_id, message.chat.id, message.message_id)

@dp.callback_query(lambda c: c.data.startswith("report_"))
async def handle_report(callback: CallbackQuery):
    _, reported_id_str, reason = callback.data.split("_")
    reported_id = int(reported_id_str)
    await bot.send_message(ADMIN_ID, f"Жалоба от {callback.from_user.id} на {reported_id}. Причина: {reason}")
    await callback.answer("Жалоба отправлена.")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())