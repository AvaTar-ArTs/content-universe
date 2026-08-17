from __future__ import annotations

from ...creativeos.operations import OperationKind
from ..contracts import ProviderToolCatalog, ProviderToolContract


IDEOGRAM_TOOL_CONTRACTS: tuple[ProviderToolContract, ...] = (
    ProviderToolContract(
        "generate_image",
        "creation",
        semantic_operation=OperationKind.GENERATE,
        description="Generate one image from explicit creative intent.",
    ),
    ProviderToolContract(
        "generate_images_bulk",
        "creation",
        semantic_operation=OperationKind.GENERATE,
        description="Generate a coordinated batch of image prompts/jobs.",
    ),
    ProviderToolContract(
        "edit_image",
        "transform",
        semantic_operation=OperationKind.EDIT,
        description="Edit referenced image content; do not silently substitute remix or generation.",
    ),
    ProviderToolContract(
        "reframe_image",
        "transform",
        semantic_operation=OperationKind.REFRAME,
        description="Change framing/canvas around exactly one source image.",
    ),
    ProviderToolContract(
        "remix_image",
        "transform",
        semantic_operation=OperationKind.REMIX,
        description="Create a variation derived from exactly one source image.",
    ),
    ProviderToolContract(
        "upscale_image",
        "transform",
        semantic_operation=OperationKind.UPSCALE,
        description="Increase resolution/detail while retaining parent lineage.",
    ),
    ProviderToolContract(
        "remove_background",
        "transform",
        semantic_operation=OperationKind.REMOVE_BACKGROUND,
        description="Create a background-removed derivative from one source image.",
    ),
    ProviderToolContract(
        "get_generation_status",
        "history",
        mutating=False,
        description="Read generation/job status.",
    ),
    ProviderToolContract(
        "get_recent_generations",
        "history",
        mutating=False,
        description="Read recent generation history for continuation workflows.",
    ),
    ProviderToolContract(
        "upload_image",
        "assets",
        description="Prepare/upload a local image reference through supported provider transport.",
    ),
    ProviderToolContract(
        "describe_image",
        "assets",
        mutating=False,
        semantic_operation=OperationKind.DESCRIBE,
        description="Describe one image through a supported provider capability.",
    ),
    ProviderToolContract("list_datasets", "training", mutating=False),
    ProviderToolContract("create_dataset", "training"),
    ProviderToolContract("upload_dataset_assets", "training"),
    ProviderToolContract("train_model", "training"),
    ProviderToolContract("list_models", "training", mutating=False),
    ProviderToolContract("get_model", "training", mutating=False),
    ProviderToolContract("list_collections", "collections", mutating=False),
    ProviderToolContract("get_images_by_collection_id", "collections", mutating=False),
    ProviderToolContract("create_collection", "collections"),
    ProviderToolContract("rename_collection", "collections"),
    ProviderToolContract(
        "delete_collection",
        "collections",
        destructive=True,
        description="Delete a collection. Asset deletion must remain a separate explicit intention.",
    ),
    ProviderToolContract("add_images_to_collection", "collections"),
    ProviderToolContract(
        "remove_images_from_collection",
        "collections",
        destructive=True,
        description="Remove collection membership; permanent asset deletion requires explicit intent.",
    ),
    ProviderToolContract("list_organizations", "organizations", mutating=False),
    ProviderToolContract("set_preferred_organization", "organizations"),
)

IDEOGRAM_TOOL_CATALOG = ProviderToolCatalog(IDEOGRAM_TOOL_CONTRACTS)
