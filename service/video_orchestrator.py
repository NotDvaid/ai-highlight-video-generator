
from typing import Callable

from service.models.requests import AssetUpload
from service.media.asset_loader import AssetLoader
from service.ai.media_analyzer import MediaAnalyzer
from service.ai.prompt_engine import accept_request
from service.ai.planner import Planner
from service.renderer.composer import Composer
from service.renderer.ffmpeg_render import FFmpegRenderer


class VideoOrchestrator:
    def __init__(self):
        self.asset_loader = AssetLoader()
        self.media_analyzer = MediaAnalyzer()
        self.planner = Planner()
        self.composer = Composer()
        self.renderer = FFmpegRenderer()

    def orchestrate(
        self,
        assets: list[AssetUpload],
        prompt: str,
        chronological: bool = False,
        progress_callback: Callable[[int, str], None] | None = None,
    ):
        # Stage 1: Validate media and extract technical metadata
        if progress_callback:
            progress_callback(5, "Loading and validating media")

        loaded_assets = [
            self.asset_loader.load(upload)
            for upload in assets
        ]

        # Stage 2: Analyze media
        if progress_callback:
            progress_callback(10, "Analyzing media")

        analysis_results = []

        for asset in loaded_assets:
            analysis_results.append(
                self.media_analyzer.analyze(asset)
            )

        # Stage 3: Generate the AI plan
        if progress_callback:
            progress_callback(40, "Planning your video")

        ai_plan = accept_request(
            prompt=prompt,
            assets=loaded_assets,
            analysis_results=analysis_results,
        )

        # Stage 4: Build the timeline
        if progress_callback:
            progress_callback(60, "Building video timeline")

        timeline = self.planner.create_timeline(
            assets=loaded_assets,
            ai_plan=ai_plan,
            chronological=chronological,
        )

        # Stage 5: Compose and render
        if progress_callback:
            progress_callback(75, "Rendering your video")

        render_plan = self.composer.compose(
            timeline=timeline
        )

        output_path = self.renderer.render(
            render_plan=render_plan
        )

        if progress_callback:
            progress_callback(100, "Video ready")

        return output_path
