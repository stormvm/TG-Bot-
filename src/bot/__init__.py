from bot.routers.main.start import router as start_router
from bot.routers.main.kab import router as kab_router
from bot.routers.admin.broadcast import router as broadcast_router
from bot.routers.admin.admin import router as admin_router
from bot.routers.another.rerun import router as rerun_router
from bot.routers.another.support import router as support_router
from bot.routers.balance.buy import router as buy_router
from bot.routers.balance.pay import router as pay_router
from bot.routers.menu.catalog import router as catalog_router

__all__ = [
    'start_router',
    'kab_router',
    'broadcast_router',
    'admin_router',
    'rerun_router',
    'support_router',
    'buy_router',
    'pay_router',
    'catalog_router'
]