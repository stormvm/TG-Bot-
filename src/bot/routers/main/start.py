from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.types import Message
from bot.routers import start_keyboard,add_user,ADMIN_ID,admin_keyboard
from bot.routers.admin.admin import start_command_admin_handler
router = Router()

@router.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    add_user(message.from_user.id)
    if int(message.from_user.id) == int(ADMIN_ID):
        await start_command_admin_handler(message)
        
    else:    
        await message.edit_text("Привет! Добро пожаловать в нашего бота!\n",   reply_markup=start_keyboard)