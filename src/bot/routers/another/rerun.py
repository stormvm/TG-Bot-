from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.routers import start_keyboard
router = Router()

@router.callback_query(F.data == "back_to_main")
async def handle_rerun_command(callback: CallbackQuery):
    await callback.message.edit_text("Возвращаю вас в меню",reply_markup=start_keyboard)