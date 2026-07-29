import subprocess
from service.media.asset_loader import AssetLoader
from service.models.requests import AssetUpload
from service.exceptions import MissingMetadataError

raise MissingMetadataError(["Duration", "Width"])
loader = AssetLoader()
uploader = AssetUpload(path="C:/Users/User/Videos/video test.mp4",media_type="mp4")

loader.load(uploader)