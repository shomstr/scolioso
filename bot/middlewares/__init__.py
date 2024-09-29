import logging

from aiogram import Dispatcher
from .database import (
    setup_get_repo_middleware,
    setup_get_user_middleware,
    setup_get_chat_middleware,
    setup_get_chat_user_middleware,
)
from .throttling import setup_throttling_middleware
from .add_foliage_user import setup_add_foliage_middleware

logger = logging.getLogger("middlewares")


def _setup_inner_middlewares(dp: Dispatcher) -> None:
    setup_throttling_middleware(dp)

    setup_get_repo_middleware(dp)
    setup_get_user_middleware(dp)
    setup_get_chat_middleware(dp)
    setup_get_chat_user_middleware(dp)

    logger.debug("middlewares was been load")


def _setup_outers_middlewares(dp: Dispatcher):
    setup_add_foliage_middleware(dp)


def setup_middlewares(dp: Dispatcher):
    _setup_outers_middlewares(dp)
    _setup_inner_middlewares(dp)


__all__ = ["setup_middlewares"]
