print("MEDIA ANALYSIS STARTED")

import os
from pathlib import Path
from service.models.asset import Asset
from service.models.asset_analysis import AssetAnalysis
from dotenv import load_dotenv
from groq import Groq
import base64
from service import exceptions
import mimetypes
from google import genai

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=api_key)

gemini_api_key = os.getenv("GEMINI_API_KEY")

gemini_client = genai.Client(api_key=gemini_api_key)

class MediaAnalyzer:
    def analyze(self, asset: Asset):
        if asset.media_type == "image":
            with open(asset.path,"rb") as image_file:
                # Read and encode the image
                # Set the path
                image_data = image_file.read()
                encode_image = base64.b64encode(image_data).decode("utf-8")
                path = Path(asset.path)

                if path.suffix.lower() in {".jpg", ".png", ".jpeg", ".webp", ".bmp"}:
                    # Determine MIME type
                    mime_type = mimetypes.guess_type(str(path))[0]
                else:
                    # Raise unsupported-format exception
                    raise exceptions.UnsupportedMediaTypeError(
                    str(path),
                    "Unsupported image format. Please use a supported image type."
                )
                if mime_type is None:
                    # Raise MIME-type exception
                    raise exceptions.UnsupportedMediaTypeError(str(path),"Cannot determine File type ")
                image_url = f"data:{mime_type};base64,{encode_image}"
                response = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    max_tokens=300,
                    messages=[
                        {
                            "role": "system",
                            "content": """
                            You are a visual media analyst for an AI highlight video generator.

                            Analyze the provided image and produce a concise, factual description
                            of its visible content.

                            Describe:
                            - The main subjects or objects.
                            - The action or activity taking place, if apparent.
                            - The setting or environment.
                            - Notable visual details that could help determine the image's
                            relevance to a user's video instructions.

                            Only describe details reasonably supported by the image.
                            Do not invent events, identities, or context. If something is
                            unclear, say so.

                            Return only the description as plain text.
                            Do not determine the order of the video or make editing decisions.
                            """
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Describe the visible content of this image."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    }
                                }
                            ]
                        }
                    ]
                )


            usage = response.usage

            prompt_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens

            prompt_cost = prompt_tokens * 0.80 / 1_000_000
            output_cost = output_tokens * 4.00 / 1_000_000
            total_cost = prompt_cost + output_cost

            print("\n--- QWEN USAGE ---")
            print(f"Prompt tokens (text + image): {prompt_tokens}")
            print(f"Output tokens: {output_tokens}")
            print(f"Total tokens: {total_tokens}")
            print(f"Estimated prompt cost: ${prompt_cost:.8f}")
            print(f"Estimated output cost: ${output_cost:.8f}")
            print(f"Estimated request cost: ${total_cost:.8f}")
            description = response.choices[0].message.content
            analysis = AssetAnalysis(
            asset_id = str(asset.asset_id),
            description = description
            )
            return analysis

        elif asset.media_type == "video":
            video_file = gemini_client.files.upload(file=asset.path)
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    video_file,
                    """
                    Analyze this video for an AI highlight video generator.

                    Describe:
                    - The main subjects.
                    - The actions taking place.
                    - Important moments that may be useful in a highlight video.

                    Only describe what is supported by the footage.
                    Return a concise description.
                    """
                ]
            )
            description = response.text
            analysis = AssetAnalysis(
                asset_id = str(asset.asset_id),
                description = description
                )
            return analysis