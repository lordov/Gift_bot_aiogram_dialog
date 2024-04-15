"""Import all routers and add them to routers_list."""

from .standart_handlers import start_router


router_list = [
    start_router
]

__all__ = [
    "routers_list"
]