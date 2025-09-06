from aiogram import Router

from .directories import router as courier_list_routes
from .courier_dirs import router as courier_menu_routes
from filters import RequireRoles

router = Router()
router.message.filter(RequireRoles("админ"))
router.callback_query.filter(RequireRoles("админ"))

router.include_router(courier_list_routes)
router.include_router(courier_menu_routes)

