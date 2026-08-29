from service.models.asset import Asset
from service.models.timeline import Timeline
from service.models.ai_plan import AIPlan


class Planner:
    def create_timeline(
        self,
        assets: list[Asset],
        ai_plan: AIPlan
    ):
        asset_lookup = {
            str(asset.asset_id): asset
            for asset in assets
        }

        ordered_assets = [
            asset_lookup[asset_id]
            for asset_id in ai_plan.asset_order
        ]

        timeline = Timeline(assets=ordered_assets)

        return timeline