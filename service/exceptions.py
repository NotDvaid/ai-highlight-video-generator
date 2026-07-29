from pathlib import Path

# Exceptions related to loading media assets

class AssetNotFoundError(Exception):
    # Raised when the requested asset file does not exist
    def __init__(self, path: str):
        self.path = path
        super().__init__("Unable to locate file:" + path)
        


class UnsupportedMediaTypeError(Exception):
    # Raised when the uploaded media type is not supported
    def __init__(self, path: str):
        self.path = path
        super().__init__("file not supported :" + path)
        

class CorruptedMediaError(Exception):
    # Raised when a media file cannot be read correctly
    def __init__(self, path: str):
        self.path = path
        super().__init__("Unable to read file:" + path)

class MissingMetadataError(Exception):
    # Raised when a there is a missing value in the metadata
    def __init__(self, missingFields):
        message = "Missing required metadata:\n"
        for field in missingFields:
           message += "- " + field +"\n"
        super().__init__(message)


            