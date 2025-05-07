from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, InputMediaVideo
from aiogram import types
from aiogram.types import Message,CallbackQuery
from bot.routers import get_user, Create_support_message,update_last_time_user,start_keyboard,save_support_message,ADMIN_ID
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
router = Router()

@router.callback_query(F.data == 'support')
async def callback_support(callback: CallbackQuery, state: FSMContext):
    dataaa = get_user(callback.from_user.id)
    for i in data:
        data = i[2]
    current_time = datetime.now()
    
    if data == 'None':
        flag = True
    else:
        try:
            # Конвертируем строку времени в datetime объект
            last_message_time = datetime.strptime(data, "%m/%d/%Y, %H:%M:%S")
            time_difference = current_time - last_message_time
            
            # Фиксированное время ожидания - 10 часов
            wait_time = timedelta(hours=10)
            time_left = wait_time - time_difference
            
            if time_left.total_seconds() <= 0:
                flag = True
            else:
                flag = False
                hours_left = time_left.total_seconds() / 3600
        except ValueError:
            print('Ошибка при конвертации времени')
            flag = False
            hours_left = 10

    if flag is True:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_main"
        ))

        await state.set_state(Create_support_message.waiting_for_message)
        await callback.message.edit_text(
            "Напишите ваше сообщение в поддержку\nВы можете прикрепить фото или видео",
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.edit_text(
            f"Вы сможете отправить следующее сообщение через {hours_left:.1f} часов",
            show_alert=True
        )


@router.message(StateFilter(Create_support_message.waiting_for_message))
async def giv_support_info(message: types.Message, state: FSMContext, album: list[Message] = None):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
    text="Отправить",
    callback_data="send_message")
    )
    builder.add(types.InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_main")
    )
    if album:  # Если это альбом
        # Создаем список медиафайлов для группы
        media = []
        photoss = []
        videos = []
        
        for msg in album:
            if msg.photo:
                media.append(InputMediaPhoto(
                    media=msg.photo[-1].file_id,
                    caption=msg.caption if msg.caption else None
                ))
                photoss.append(msg.photo[-1].file_id)
            if msg.video:
                media.append(InputMediaVideo(
                    media=msg.video.file_id,
                    caption=msg.caption if msg.caption else None
                ))
                videos.append(msg.video.file_id)
        
        text = next((msg.caption for msg in album if msg.caption), None)
        
        # Отправляем медиагруппу
        await message.answer_media_group(media=media)
        # Отправляем кнопки отдельным сообщением
        await message.answer("Подтвердите отправку:", reply_markup=builder.as_markup())
        
        # Save to state with consistent keys
        await state.update_data(
            photos=photoss if photoss else None,
            videos=videos if videos else None,
            text=text if text else None
        )
    else:  # Если одиночное сообщение
        await message.copy_to(chat_id=message.chat.id,reply_markup=builder.as_markup())
        
        if message.photo:
            await state.set_state(Create_support_message.pictures)
            await state.update_data(
                photos=[message.photo[-1].file_id],
                caption=message.caption if message.caption else None
            )
        elif message.video:
            await state.set_state(Create_support_message.videos)
            await state.update_data(
                videos=[message.video.file_id],
                caption=message.caption if message.caption else None
            )
        elif message.text:
            await state.set_state(Create_support_message.waiting_for_message)
            await state.update_data(text=message.text)                    
    await state.set_state(Create_support_message.send)        
    
@router.callback_query(F.data == 'send_message', StateFilter(Create_support_message.send))
async def send_support_message(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print("State data:", data)  # Debug print
    
    user_id = callback.from_user.id
    photos = data.get('photos', [])  # Changed from 'pictures' to 'photos'
    videos = data.get('videos', [])
    text = data.get('text')  # Changed from 'waiting_for_message' to 'text'
    
    print("Photos:", photos)  # Debug print
    print("Videos:", videos)  # Debug print
    print("Text:", text)  # Debug print
    
    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    # Сохраняем сообщение в базу данных
    message_id = save_support_message(
        user_id=user_id,
        photos=photos if photos else None,
        videos=videos if videos else None,
        text=text if text else None
    )
    
    # Отправляем подтверждение пользователю
    await callback.message.edit_text(f"Ваше сообщение #{message_id} отправлено в поддержку")
    await callback.message.delete()
    
    # Сохраняем время последнего сообщения
    update_last_time_user(user_id, date)
    
    # Отправляем сообщение администратору (можно заменить на ID админ-чата)
    admin_chat_id = ADMIN_ID  # Замените на реальный ID админ-чата
    
    # Формируем сообщение для админа
    admin_text = f"Новое сообщение #{message_id}\nОт пользователя: {user_id}\n"
    if text:
        admin_text += f"Текст: {text}\n"
    await callback.bot.send_message(admin_chat_id, admin_text)
    
    # Отправляем медиафайлы администратору
    if photos:
        media = [InputMediaPhoto(media=photo) for photo in photos]
        await callback.bot.send_media_group(admin_chat_id, media=media)
    
    if videos:
        media = [InputMediaVideo(media=video) for video in videos]
        await callback.bot.send_media_group(admin_chat_id, media=media)
    
    # Очищаем состояние
    await state.clear()
    await callback.message.answer("Возвращаю вас в меню",reply_markup=start_keyboard)