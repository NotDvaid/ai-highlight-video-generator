from pydantic import BaseModel
from service.models.asset import Asset

class Timeline(BaseModel):
    assets : list[Asset]