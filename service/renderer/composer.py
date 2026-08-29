# Responsibilities:
#
# 1. Receive Timeline.
# 2. Analyze the Timeline.
# 3. Create a RenderPlan.
# 4. Return the RenderPlan.
# Remeber:
# Classes describe what an object will look like.
# Objects contain the actual data.
#
# Timeline = the blueprint (class/type)
# timeline = the actual Timeline object passed into compose()
from pydantic import BaseModel
from service.models.timeline import Timeline
from service.models.render_plan import RenderPlan


class Composer:
    def compose(self, timeline: Timeline) -> RenderPlan:

        build_render_plan =  RenderPlan(timeline= timeline)

        return build_render_plan