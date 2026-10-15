from pydantic import BaseModel


class AssetAnalysis(BaseModel):
    asset_id: str
    description: str