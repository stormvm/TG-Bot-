from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.types import Message
from bot.routers import start_keyboard,add_user
router = Router()

@router.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("Привет! Добро пожаловать в нашего бота!\n",reply_markup=start_keyboard)