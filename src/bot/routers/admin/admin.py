from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.routers import get_user,ADMIN_ID,admin_keyboard
router = Router()

@router.message(F.text == "/start")
async def start_command_handler(message: Message):
  if message.from_user.id == ADMIN_ID:
    await message.answer("Привет! Добро пожаловать в нашего бота!\n",reply_markup=admin_keyboard)

