from pydantic import BaseModel


class AIPlan(BaseModel):
    asset_order: list[str]