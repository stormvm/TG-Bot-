from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.routers import get_all_active_users,BroadcastStates

router = Router()


@router.callback_query(F.data == "broadcast")
async def broadcast_message(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_main"
    ))
    await callback.message.answer(
        text="Введите текст сообщения для рассылки\nМожно добавить фото или видео",
        reply_markup=builder.as_markup()
    )
    await state.set_state(BroadcastStates.waiting_for_message)
@router.message(StateFilter(BroadcastStates.waiting_for_message))
async def es_or_not_boardcast(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Да",
        callback_data="yes_broadcast"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Нет",
        callback_data="back_to_main"
    ))
    await message.answer(
        text="Вы хотите отправить это сообщение всем пользователям?",
        reply_markup=builder.as_markup()
    )
    await state.update_data(broadcast_message=message)
    await state.set_state(BroadcastStates.send)
    
@router.callback_query(F.data == "yes_broadcast",StateFilter(BroadcastStates.send))
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get('broadcast_message')
    active_users = get_all_active_users()
    sent_count = 0
    failed_count = 0
    
    try:
        for user_id in active_users:
            try:
                if message.photo:
                    await callback.bot.send_photo(
                        user_id,
                        message.photo[-1].file_id,
                        caption=message.caption
                    )
                elif message.video:
                    await callback.bot.send_video(
                        user_id,
                        message.video.file_id,
                        caption=message.caption
                    )
                elif message.text:
                    await callback.bot.send_message(user_id, message.text)
                sent_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to send to {user_id}: {e}")
        
        await callback.message.edit_text(
            f"Рассылка завершена!\n"
            f"✅ Успешно отправлено: {sent_count}\n"
            f"❌ Не удалось отправить: {failed_count}"
        )
    
    except Exception as e:
        await callback.message.edit_text(f"Произошла ошибка при рассылке: {e}")
    
    finally:
        await state.clear()
        await callback.message.delete()