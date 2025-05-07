from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

control_users_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
           [InlineKeyboardButton(text="Посмотреть профиль пользователя", callback_data="user_info")],
           [InlineKeyboardButton(text="Заблокировать пользователя", callback_data="user_block")],
           [InlineKeyboardButton(text="Разблокировать пользователя", callback_data="user_unblock")]
    ]
)