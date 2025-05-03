from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Create_support_message(StatesGroup):
    waiting_for_message = State()
    pictures = State()
    videos = State()
    send = State()