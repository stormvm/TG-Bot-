from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    send = State()