__all__ = ["router"]
from .details_views import router as details_views_router
from .list_views import router

router.include_router(details_views_router)
