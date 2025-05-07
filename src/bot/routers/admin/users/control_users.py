from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.routers import get_user,kabinet_keyboard,control_users_keyboard,admin_keyboard,user_mn,Get_info_user,block_user,unblock_user
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
router = Router()

@router.callback_query(F.data == "control_users")
async def cabinet_command_handler(callback: CallbackQuery):
  await callback.message.answer(
    text="Что вы хотите сделать?",
    reply_markup=control_users_keyboard
  )
  
@router.callback_query(F.data == "user_info")
async def user_info(callback: CallbackQuery,state: FSMContext):
  await callback.message.answer(
    text="Введите ID пользователя, информацию о котором хотите получить"
  )
  await state.set_state(Get_info_user.User_id)
  
@router.message(StateFilter(Get_info_user.User_id))
async def get_info_from_user(message: Message,state: FSMContext):
  user_id = message.text
  if user_id.isdigit():
    try:
      info = get_user(int(user_id))
      for i in info:
        id = i[0]
        balance = i[1]
        last_msg_sup = i[2]
        await message.answer(
        text=f"Информация о пользователе:\n"
        f"ID: <code>{id}</code>\n"
        f"Баланс: <code>{balance}</code>\n"
        f"Последнее сообщение в поддержку: <code>{last_msg_sup}</code>",
        reply_markup=admin_keyboard
        )
    except Exception as e:
      await message.answer(
        text=f"Ошибка: {e}")
          
  else:
    await message.answer(
      text="ID пользователя должен быть числом!",
      reply_markup=ReplyKeyboardRemove()
    )
  await state.clear()
  
@router.callback_query(F.data == "user_block")
async def user_block(callback: CallbackQuery,state: FSMContext):
  await callback.message.answer(
    text="Введите ID пользователя, которого хотите заблокировать"
  )
  await state.set_state(block_user.User_id)
  
@router.message(StateFilter(block_user.User_id))
async def block_user(state: FSMContext,message: Message):
   user_id = message.text
   if user_id.isdigit():
     try:
       user_mn(1,user_id)
       await message.answer(
         text=f"Пользователь {user_id} успешно заблокирован",
         reply_markup=admin_keyboard
       )
     except Exception as e:
       await message.answer(
         text=f"Ошибка: {e}")
   else:
     await message.answer(
       text="ID пользователя должен быть числом!",
       reply_markup=ReplyKeyboardRemove()
     )   

@router.callback_query(F.data == "user_unblock")
async def user_block(callback: CallbackQuery,state: FSMContext):
  await callback.message.answer(
    text="Введите ID пользователя, которого хотите разблокировать"
  )
  await state.set_state(unblock_user.User_id)
  
@router.message(StateFilter(unblock_user.User_id))
async def block_user(state: FSMContext,message: Message):
   user_id = message.text
   if user_id.isdigit():
     try:
       user_mn(0,user_id)
       await message.answer(
         text=f"Пользователь {user_id} успешно разблокирован",
         reply_markup=admin_keyboard
       )
     except Exception as e:
       await message.answer(
         text=f"Ошибка: {e}")
   else:
     await message.answer(
       text="ID пользователя должен быть числом!",
       reply_markup=ReplyKeyboardRemove()
     )   
   await state.clear()  