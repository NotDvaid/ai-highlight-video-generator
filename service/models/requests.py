from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AssetUpload(BaseModel):
    asset_id: UUID
    path: str
    media_type: str
    capture_time: datetime | None = None


class CreateVideoRequest(BaseModel):
    assets: list[AssetUpload]
    prompt: str