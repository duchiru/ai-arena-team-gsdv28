from app.routers.categories import router as categories_router
from app.routers.components import router as components_router
from app.routers.validation import router as validation_router
from app.routers.outfits import router as outfits_router
from app.routers.suggestions import router as suggestions_router
from app.routers.images import router as images_router
from app.routers.uploads import router as uploads_router
from app.routers.lookbooks import router as lookbooks_router
from app.routers.compare import router as compare_router

all_routers = [
    categories_router,
    components_router,
    validation_router,
    outfits_router,
    suggestions_router,
    images_router,
    uploads_router,
    lookbooks_router,
    compare_router,
]

__all__ = ["all_routers"]
