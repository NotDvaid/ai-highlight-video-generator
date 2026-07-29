from pydantic import BaseModel
from uuid import UUID

class Asset(BaseModel):
        asset_id: UUID
        path: str
        media_type: str
        duration: float
        width: int
        height: int
        has_audio: bool
        fps: float


