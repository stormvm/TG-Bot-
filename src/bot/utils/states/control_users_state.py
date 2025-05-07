from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Get_info_user(StatesGroup):
    User_id = State()
    
class block_user(StatesGroup):
    User_id = State()

class unblock_user(StatesGroup):
    User_id = State()        