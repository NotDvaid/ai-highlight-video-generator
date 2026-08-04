from service.models.asset import Asset
from service.renderer.timeline import Timeline

class Planner:
    def create_timeline(self, assets: list[Asset]):
         
        timeline = Timeline(assets=assets)
       
        return timeline  