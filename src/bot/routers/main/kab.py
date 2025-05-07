from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.routers import get_user,kabinet_keyboard
router = Router()

@router.callback_query(F.data == "kabinet")
async def cabinet_command_handler(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id) 
    balance = user_data[1] if user_data else 0  
    await callback.message.edit_text(
        f"Привет, вот твой личный кабинет!\n"
        f"Юзер: {callback.from_user.id}\n"
        f"Баланс: {balance} руб.",
        reply_markup=kabinet_keyboard
    )