from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.routers import get_user,ADMIN_ID,admin_keyboard

async def start_command_admin_handler(message: Message):
  await message.edit_text("Привет! Добро пожаловать в нашего бота!\n",reply_markup=admin_keyboard)