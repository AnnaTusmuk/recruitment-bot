import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from db import init_db, add_candidate, get_all_candidates

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ADMIN_PHONES = [
    "+380930893174",  # HR
    "+380669367339",  # Sales
    "+380990955433",  # Owner
    "+380689540033"   # New Admin
]

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.add("View Candidates", "Register Candidate")

candidate_menu = ReplyKeyboardMarkup(resize_keyboard=True)
candidate_menu.add("Register Profile")

user_phones = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    contact_button = KeyboardButton("Share Contact", request_contact=True)
    contact_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_menu.add(contact_button)
    await message.answer("Please share your contact number to continue:", reply_markup=contact_menu)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = f"+{phone}"
    user_phones[message.from_user.id] = phone

    if phone in ADMIN_PHONES:
        await message.answer("Welcome, Admin! Choose an action:", reply_markup=admin_menu)
    else:
        await message.answer("Welcome! Use the menu below:", reply_markup=candidate_menu)

@dp.message_handler(lambda message: message.text == "Register Candidate")
async def register_candidate(message: types.Message):
    await message.answer("Candidate registration will be implemented soon.")

@dp.message_handler(lambda message: message.text == "View Candidates")
async def view_candidates(message: types.Message):
    candidates = get_all_candidates()
    if candidates:
        text = "\n\n".join([f"{c[1]} ({c[2]})" for c in candidates])
        await message.answer(f"Registered Candidates:\n{text}")
    else:
        await message.answer("No candidates yet.")

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp, skip_updates=True)