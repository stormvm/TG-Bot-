from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

kabinet_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
           [InlineKeyboardButton(text="Назад", callback_data="back_to_main")],
           [InlineKeyboardButton(text="Пополнить баланс", callback_data="top_up_balance")]
    ]
)