from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.types import Message

router = Router()

@router.message(F.text & F.command("pay"))
async def process_payment_command(message: types.Message):
    await message.answer("Please provide the payment details.") 

@router.message(F.text & F.command("confirm_payment"))
async def confirm_payment_command(message: types.Message):
    await message.answer("Your payment has been confirmed.") 

@router.message(F.text & F.command("cancel_payment"))
async def cancel_payment_command(message: types.Message):
    await message.answer("Your payment has been canceled.") 

@router.callback_query(F.data.startswith("pay_"))
async def process_payment_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Processing your payment...")