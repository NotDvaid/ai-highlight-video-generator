
from service.models.asset import Asset
from service.models.timeline import Timeline
from service.models.ai_plan import AIPlan


class Planner:
    def create_timeline(
        self,
        assets: list[Asset],
        ai_plan: AIPlan,
        chronological: bool = False,
    ):
        if chronological:
            if any(asset.capture_time is None for asset in assets):
                raise ValueError(
                    "Chronological ordering requires a capture_time "
                    "for every asset."
                )

            ordered_assets = sorted(
                assets,
                key=lambda asset: asset.capture_time,
            )
        else:
            asset_lookup = {
                str(asset.asset_id): asset
                for asset in assets
            }

            ordered_assets = [
                asset_lookup[asset_id]
                for asset_id in ai_plan.asset_order
            ]

        return Timeline(assets=ordered_assets)
