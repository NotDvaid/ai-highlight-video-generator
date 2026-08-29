from service.models.timeline import Timeline
from pydantic import BaseModel

class RenderPlan(BaseModel):
    timeline: Timeline