from pydantic import BaseModel

class AssetUpload(BaseModel):
    path: str
    media_type: str

class CreateVideoRequest(BaseModel):
    assets: list[AssetUpload]
    prompt: str