from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from collections import defaultdict
import asyncio

class AlbumMiddleware(BaseMiddleware):
    def __init__(self, latency: float = 0.5):  # Увеличили задержку
        self.latency = latency
        self.album_data = defaultdict(list)
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.album_data[event.media_group_id].append(event)
            
            # Ждем, пока соберутся все медиафайлы альбома
            await asyncio.sleep(self.latency)
            
            # Проверяем, это первое сообщение из альбома?
            if event.message_id != self.album_data[event.media_group_id][0].message_id:
                return
            
            # Передаем все сообщения альбома в handler
            data['album'] = self.album_data[event.media_group_id]
            result = await handler(event, data)
            
            # Очищаем данные альбома
            del self.album_data[event.media_group_id]
            
            return result
        except Exception as e:
            print(f"Error in AlbumMiddleware: {e}")
            return await handler(event, data)