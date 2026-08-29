print("PROMPT ENGINE STARTED")

from dotenv import load_dotenv
import os
from groq import Groq
from service.models.asset import Asset
from pydantic import BaseModel
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

class AIPlan(BaseModel):
    asset_order: list[str]


def accept_request(prompt: str, assets: list[Asset]):
    asset_info = []

    for asset in assets:
        asset_info.append({
            "asset_id": str(asset.asset_id),
            "media_type": asset.media_type,
            "duration": asset.duration
        })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
    You are a video editing planner.

    Given a user's video editing request and a list of available assets,
    decide the order the assets should appear in the final video.

    Return ONLY valid JSON in this exact format:

    {
        "asset_order": ["asset_id_1", "asset_id_2"]
    }

    Use the exact asset IDs provided.
    Do not create new IDs.
    Do not include explanations.
    """
            },
            {
                "role": "user",
                "content": f"User request: {prompt}\nAvailable assets: {asset_info}"
            }
        ]
    )

    print(response.choices[0].message.content)
    ai_data = json.loads(response.choices[0].message.content)

    ai_plan = AIPlan(**ai_data)

    print(ai_plan)

    return ai_plan





    
