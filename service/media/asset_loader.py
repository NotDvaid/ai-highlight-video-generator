
import json
import subprocess
from pathlib import Path

from service.models.requests import AssetUpload
from service.models.asset import Asset
from service import exceptions


class AssetLoader:
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

    def load(self, upload: AssetUpload) -> Asset:
        path = Path(upload.path)

        if not path.is_file():
            raise exceptions.AssetNotFoundError(str(path))

        extension = path.suffix.lower()

        if extension not in self.IMAGE_EXTENSIONS | self.VIDEO_EXTENSIONS:
            raise exceptions.UnsupportedMediaTypeError(str(path))

        metadata = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-print_format", "json",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

        if metadata.returncode != 0:
            raise exceptions.CorruptedMediaError(str(path))

        try:
            data = json.loads(metadata.stdout)
        except json.JSONDecodeError as error:
            raise exceptions.CorruptedMediaError(str(path)) from error

        streams = data.get("streams", [])

        if not streams:
            raise exceptions.MissingMetadataError(["Streams"])

        is_image = extension in self.IMAGE_EXTENSIONS

        video_stream = next(
            (stream for stream in streams
             if stream.get("codec_type") == "video"),
            None,
        )

        if video_stream is None:
            raise exceptions.MissingMetadataError(["Video stream"])

        width = video_stream.get("width")
        height = video_stream.get("height")

        if is_image:
            duration = 5.0
            fps = 0.0
            has_audio = False
            media_type = "image"
        else:
            duration_value = (
                video_stream.get("duration")
                or data.get("format", {}).get("duration")
            )

            try:
                duration = float(duration_value)
            except (TypeError, ValueError):
                duration = 0.0

            if duration <= 0:
                raise exceptions.MissingMetadataError(["Duration"])

            fps_value = video_stream.get("avg_frame_rate", "0/0")

            try:
                numerator, denominator = fps_value.split("/")
                denominator = float(denominator)

                if denominator == 0:
                    raise ValueError("Invalid frame-rate denominator")

                fps = float(numerator) / denominator
            except (ValueError, ZeroDivisionError):
                raise exceptions.MissingMetadataError(["AverageFps"])

            has_audio = any(
                stream.get("codec_type") == "audio"
                for stream in streams
            )
            media_type = "video"

        missing_fields = []

        if width is None:
            missing_fields.append("Width")

        if height is None:
            missing_fields.append("Height")

        if missing_fields:
            raise exceptions.MissingMetadataError(missing_fields)

        return Asset(
            asset_id=upload.asset_id,
            path=str(path),
            media_type=media_type,
            duration=duration,
            width=int(width),
            height=int(height),
            has_audio=has_audio,
            fps=fps,
            capture_time=upload.capture_time,
        )
