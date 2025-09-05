from aiogram import Router
from .controller_auth import router as admin
from .courier_auth import router as courier
from .profile_routes import router as profile
from .registration import router as reg
from .start_cmd import router as start

router = Router()

router.include_router(admin)
router.include_router(courier)
router.include_router(profile)
router.include_router(reg)
router.include_router(start)

