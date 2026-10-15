from service.media.asset_loader import AssetLoader
from service.models.requests import AssetUpload
from service.ai.media_analyzer import MediaAnalyzer
from service.ai.prompt_engine import accept_request
from service.ai.planner import Planner
from service.renderer.composer import Composer
from service.renderer.ffmpeg_render import FFmpegRenderer

# Responsibilities:
#
# 1. Receive the video creation request from the route.
# 2. Call AssetLoader to validate and load uploaded media.
# 3. Receive the validated Asset objects.
# 4. Coordinate media analysis for the uploaded assets.
# 5. Receive AssetAnalysis results from the media analyzer.
# 6. Pass the assets and analysis results to the Planner.
# 7. Receive the Timeline containing the planned asset order.
# 8. Call Composer to create a RenderPlan from the Timeline.
# 9. Call Renderer to generate the final video.
# 10. Receive the finished video.
# 11. Return the video response to the route.
#
# TODO (Future Features):
#
# - Analyze video frames and GIFs for visual content.
# - Improve error handling for invalid or unsupported media.
# - Use AI analysis results to improve asset selection and ordering.
# - Integrate persistent storage for uploaded and rendered media.
#

class VideoOrchestrator:
    def __init__(self):
        self.media_analyzer = MediaAnalyzer()
        self.loader = AssetLoader()
        self.planner = Planner()
        self.composer = Composer()
        self.renderer = FFmpegRenderer()

    def orchestrate(self, uploads: list[AssetUpload], prompt):
        assets = []
        analysis_results = []


        for upload in uploads:
            assets.append(self.loader.load(upload))

        for asset in assets:
            analysis_results.append(self.media_analyzer.analyze(asset))

        ai_plan = accept_request(prompt=prompt,  assets=assets)
        timeline = self.planner.create_timeline(assets=assets, ai_plan=ai_plan)
        render_plan = self.composer.compose(timeline=timeline)
        output_path = self.renderer.render(render_plan=render_plan)

        return output_path