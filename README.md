# Impact Reels

Impact Reels is an AI-powered video highlight generator designed to help users quickly turn photos and videos from events into short, engaging highlight videos.

The application allows users to upload their media, provide a description of the event or desired video, and have AI determine how the uploaded assets should be organized. The backend then creates a video plan and uses FFmpeg to render the final highlight video.

The goal of Impact Reels is to reduce the amount of time and technical knowledge required to create polished event highlight videos.

---

# Repo Location

[GitHub Repository](YOUR_GITHUB_REPO_URL)

---

# Project Prototype

[Figma Prototype](YOUR_FIGMA_URL)

---

# Progress Tracking Tool

[Jira Board]((https://airozdigital.atlassian.net/jira/software/projects/SOF/boards/100/backlog))

---

# Project Status

**Current Status: V1 Prototype / Active Development**

The core backend pipeline has been implemented and successfully tested with uploaded images.

Current working pipeline:

**Upload Media → Validate Assets → AI Planning → Timeline → Render Plan → FFmpeg → MP4 Video**

---

# What Has Been Completed

## Frontend

- User upload interface
- Uploading multiple images/videos
- Event/video description input
- Generate Video interaction
- Frontend-to-backend request flow
- Initial UI prototype created using Figma/V0

## Backend

### Asset Upload

- Receives uploaded media from the frontend
- Stores uploaded files
- Creates backend-controlled asset information

### Asset Loader

The `AssetLoader` validates uploaded media and extracts metadata using FFprobe.

Currently handled metadata includes:

- Asset ID
- File path
- Media type
- Duration
- Width
- Height
- Audio availability
- FPS

The loader also handles invalid or missing media metadata through custom exceptions.

### AI Planning

The AI prompt engine is currently capable of analyzing the uploaded assets and returning an asset order based on the user's prompt.

For example:

> "Put number 2 first, number 1 second, and number 3 last."

The AI can return the corresponding asset IDs in the requested order.

### Timeline

The planner converts the AI-generated plan into a timeline containing the selected assets and their order.

### Render Plan

A render plan is generated from the timeline and passed to the renderer.

### FFmpeg Renderer

The FFmpeg renderer currently:

- Accepts a render plan
- Reads assets from the timeline
- Handles image inputs
- Scales media to a vertical `720x1280` format
- Preserves aspect ratio
- Adds padding when necessary
- Assigns image durations
- Concatenates the assets
- Encodes the final video using H.264
- Produces an MP4 file

The current prototype has successfully rendered a multi-image highlight video.

---

# Current Architecture

```text
Frontend
    |
    v
CreateVideoRequest
    |
    v
Asset Upload
    |
    v
AssetLoader
    |
    v
Asset
    |
    v
AI Prompt Engine
    |
    v
AI Plan
    |
    v
Planner
    |
    v
Timeline
    |
    v
RenderPlan
    |
    v
FFmpeg Renderer
    |
    v
MP4 Highlight Video
