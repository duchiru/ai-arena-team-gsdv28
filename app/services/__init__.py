from app.services.component_service import (
    get_all_categories,
    get_category_by_id,
    get_components,
    get_component_by_id,
)
from app.services.validation_service import validate_combination
from app.services.outfit_service import (
    create_outfit,
    get_outfit,
    list_outfits,
    delete_outfit,
    regenerate_image,
)
from app.services.suggestion_service import (
    suggest_by_prompt,
    suggest_by_occasion_weather,
    check_color_harmony,
)
from app.services.image_service import (
    generate_image_custom,
    try_on_outfit,
)
from app.services.upload_service import (
    handle_upload,
    get_upload,
    delete_upload,
)
from app.services.compare_service import compare_outfits
from app.services.lookbook_service import (
    create_lookbook,
    get_lookbook_by_id,
    get_lookbook_by_share_code,
    list_lookbooks,
    add_outfit_to_lookbook,
    remove_outfit_from_lookbook,
    delete_lookbook,
)

__all__ = [
    "get_all_categories",
    "get_category_by_id",
    "get_components",
    "get_component_by_id",
    "validate_combination",
    "create_outfit",
    "get_outfit",
    "list_outfits",
    "delete_outfit",
    "regenerate_image",
    "suggest_by_prompt",
    "suggest_by_occasion_weather",
    "check_color_harmony",
    "generate_image_custom",
    "try_on_outfit",
    "handle_upload",
    "get_upload",
    "delete_upload",
    "compare_outfits",
    "create_lookbook",
    "get_lookbook_by_id",
    "get_lookbook_by_share_code",
    "list_lookbooks",
    "add_outfit_to_lookbook",
    "remove_outfit_from_lookbook",
    "delete_lookbook",
]
