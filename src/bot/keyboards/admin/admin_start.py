from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
           [InlineKeyboardButton(text="Управление пользователями", callback_data="control_users")],
           [InlineKeyboardButton(text="Запросы в поддержку", callback_data="messages_on_suopport")],
           [InlineKeyboardButton(text="Трафик", callback_data="trafic")],
           [InlineKeyboardButton(text="Рассылка", callback_data="broadcast")],
    ]
)