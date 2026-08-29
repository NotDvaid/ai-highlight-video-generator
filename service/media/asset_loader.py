import subprocess
import json
from pathlib import Path
from service.models.requests import AssetUpload
from service.models.asset import Asset
from service import exceptions
from uuid import uuid4


class AssetLoader:
    def load(self, upload: AssetUpload) -> Asset:
        # 1. Convert the uploaded path string into a Path object
        path = Path(upload.path)

       # 2. Verify the file exists. Stop immediately if it doesn't.
        if not path.exists():
            raise exceptions.AssetNotFoundError(path)

        # 3. Run ffprobe to retrieve the media metadata.
        metadata = subprocess.run(["ffprobe","-v", "quiet", "-show_format","-show_streams", "-print_format" , "json", path ], capture_output=True, text=True)
        # 3A. Ensure ffprobe completed successfully.
        if metadata.returncode == 0:
            data =  json.loads(metadata.stdout)
        else: 
            print(metadata.stderr)
            raise exceptions.CorruptedMediaError(path)
        
        
        # 4. Parse the ffprobe metadata into Asset fields.
        # 4A. Initialize placeholders for the Asset metadata.
        asset_type = None
        asset_duration = None
        asset_width = None
        asset_height = None
        asset_fps = None
        asset_audio = False
        missing_fields = []
        # 4B. Iterate through every stream returned by ffprobe.
        for stream in data["streams"]:
        # 4C. Extract metadata from the video stream.
        # 4D. Mark the asset as containing audio if an audio stream exists.
            if path.suffix in {".jpg", ".png", ".jpeg", ".webp", ".bmp"}:
                asset_type = "image"
                asset_duration = 5.0
                asset_width = stream['width']
                asset_height = stream['height']
                asset_fps = 0.0
                asset_audio = False
            elif stream['codec_type'] == 'audio':
                asset_audio = True 
            elif stream['codec_type'] == 'video':
                asset_type = stream['codec_type']
                asset_duration = stream['duration']
                asset_width = stream['width']
                asset_height = stream['height']
                asset_fps = stream['avg_frame_rate']
        if asset_duration is None:
           missing_fields.append("Duration")
        if asset_width is None:
           missing_fields.append("Width")
        if asset_height is None:
           missing_fields.append("Height")
        if asset_fps is None:
           missing_fields.append("AverageFps")
        if missing_fields != []:
            raise exceptions.MissingMetadataError(missing_fields)

        asset_id = uuid4()
       
        # 5. Build an Asset object using the metadata.
        build_Asset = Asset(asset_id= asset_id, path= path, media_type= asset_type, duration= asset_duration, width= asset_width, height= asset_height, has_audio= asset_audio, fps= asset_fps)

        # 6. Return the completed Asset.
        return build_Asset
    
        
        
        