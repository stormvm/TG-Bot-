from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
           [InlineKeyboardButton(text="Каталог товаров", callback_data="katalog")],
           [InlineKeyboardButton(text="Личный кабинет", callback_data="kabinet")],
           [InlineKeyboardButton(text="О боте", callback_data="about")],
           [InlineKeyboardButton(text="Поддержка", callback_data="support")]
    ]
)