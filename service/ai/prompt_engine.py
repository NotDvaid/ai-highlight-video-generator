print("PROMPT ENGINE STARTED")

from dotenv import load_dotenv
import os
from pathlib import Path
from groq import Groq
from service.models.asset import Asset
from pydantic import BaseModel
from service.models.asset_analysis import AssetAnalysis
import json

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

class UserIntent(BaseModel):
    exclusion_requested: bool
    reuse_requested: bool

class AIPlan(BaseModel):
    asset_order: list[str]
    excluded_assets: list[str] = []
    exclusion_requested: bool
    reuse_requested: bool

def analyze_user_intent(prompt: str) -> UserIntent:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
Determine whether the user's request explicitly authorizes
excluding uploaded assets or repeating assets.

Rules:
- exclusion_requested is true only if the user explicitly asks
  to exclude assets or restrict the video to a specific selection.
- reuse_requested is true only if the user explicitly asks
  for an asset to appear more than once.
- Do not infer permission from your own editing preferences.
- Return only valid JSON with these two boolean fields:
{"exclusion_requested": false, "reuse_requested": false}
"""
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    print("INTENT RESPONSE:", repr(content))

    if not content:
        raise ValueError("Intent model returned an empty response.")

    intent_data = json.loads(content)

    return UserIntent(**intent_data)

def accept_request(prompt: str, assets: list[Asset], analysis_results: list[AssetAnalysis]):
    user_intent = analyze_user_intent(prompt)
    asset_info = []

    for asset in assets:
        description = ""
        for analysis in analysis_results:
            if str(asset.asset_id) == analysis.asset_id:

               description = analysis.description
        asset_info.append({
            "asset_id": str(asset.asset_id),
            "media_type": asset.media_type,
            "duration": asset.duration,
            "description": description

            })


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
                You are a video editing planner.

                Use the asset descriptions and the user's editing request to choose the most logical order for the video.

                Given a user's video editing request and a list of available assets, decide the order the assets should appear in the final video.

                Follow these asset selection rules:
                - By default, include every uploaded asset exactly once.
                - Only exclude an asset when the user explicitly asks to exclude it or asks to use only a specific selection of assets.
                - Only repeat an asset when the user explicitly requests that the same asset appear more than once or at different points in the video.
                - Do not independently omit or repeat assets based on your own preferences.
                - Use the asset descriptions and the user's request to determine the most logical sequence.

                Exclusion reporting rules:
                - Set exclusion_requested to true only when the user's request explicitly asks to exclude assets or restrict the video to a specific selection.
                - Set exclusion_requested to false when the user has not explicitly requested exclusions.
                - If exclusion_requested is false, excluded_assets must be an empty list.
                - Every ID in excluded_assets must be a valid uploaded asset ID.
                - Every uploaded asset must appear in asset_order or excluded_assets.
                - No asset may appear in both asset_order and excluded_assets.
                - Do not treat your own editing preferences as user authorization to exclude assets.

                Reuse reporting rules:
                - Set reuse_requested to true only when the user's request explicitly asks for an asset to appear more than once.
                - Set reuse_requested to false when the user has not explicitly requested asset reuse.
                - If reuse_requested is false, do not repeat asset IDs in asset_order.
                - If reuse_requested is true, repeated IDs are allowed only for assets the user explicitly requested to reuse.

                Return ONLY valid JSON in this exact format:

                {
                    "asset_order": ["asset_id_1", "asset_id_2"],
                    "excluded_assets": [],
                    "exclusion_requested": false,
                    "reuse_requested": false
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
    uploaded_ids = {str(asset.asset_id) for asset in assets}
    ai_ids = set(ai_plan.asset_order)
    invalid_ids = ai_ids - uploaded_ids
    invalid_exclusions = set(ai_plan.excluded_assets) - uploaded_ids
    overlapping_ids = ai_ids & set(ai_plan.excluded_assets)
    if overlapping_ids:
        raise ValueError(f"Assets cannot be both included and excluded: {overlapping_ids}")
    if invalid_exclusions:
        raise ValueError(f"AI returned invalid excluded asset IDs: {invalid_exclusions}")
    if invalid_ids:
        raise ValueError(f"AI returned invalid asset IDs: {invalid_ids}")
    
    missing_ids = uploaded_ids - ai_ids - set(ai_plan.excluded_assets)
    if missing_ids:
        raise ValueError(f"AI omitted uploaded asset IDs: {missing_ids}")
    if len(ai_plan.asset_order) != len(ai_ids) and not ai_plan.reuse_requested:
        raise ValueError("AI returned duplicate asset IDs without an explicit reuse request.")
    if ai_plan.exclusion_requested != user_intent.exclusion_requested:
        raise ValueError("AI plan's exclusion decision does not match the user's intent.")

    if ai_plan.reuse_requested != user_intent.reuse_requested:
        raise ValueError("AI plan's reuse decision does not match the user's intent.")
    if ai_plan.excluded_assets and not user_intent.exclusion_requested:
        raise ValueError("Assets cannot be excluded without user authorization.")
    print(ai_plan)

    return ai_plan






