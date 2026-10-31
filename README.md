# Impact Reels

Impact Reels is an AI-powered video highlight generator designed to help users quickly turn photos and videos from events into short, engaging highlight videos.

The application allows users to upload their media, provide a description of the event or desired video, and have AI help determine how the uploaded assets should be organized. The backend creates a video plan and uses FFmpeg to render the final highlight video.

The goal of Impact Reels is to reduce the amount of time and technical knowledge required to create polished event highlight videos.

---

## Repository

[GitHub Repository](https://github.com/NotDvaid/ai-highlight-video-generator)

## Project Prototype

[Impact Reels Prototype – Figma Make](https://www.figma.com/make/12jft4dtpVvYSzr8jGsIlZ/Impact-Reels-Prototype?p=f&t=mStuy9ffjMaspX3M-0)

## Progress Tracking

[SoftwareDevProject – Jira Backlog](https://airozdigital.atlassian.net/jira/software/projects/SOF/boards/100/backlog)

---

## Project Status

**Current Status: V1 Prototype / Active Development**

The core backend pipeline has been implemented and successfully tested with uploaded images.

Current tested image-generation workflow:

**Upload Media → Validate Assets → AI Planning → Timeline → Render Plan → FFmpeg → MP4 Video**

Video uploads are supported by the application, but video-processing reliability and broader media compatibility still require testing.

---

## What Has Been Completed

### Frontend

- User upload interface
- Multiple image and video upload support
- Event and video description input
- Generate Video interaction
- Frontend-to-backend request flow
- Initial UI prototype created using Figma/V0
- Video generation progress display
- Generated video preview and download

### Backend

#### Asset Upload

- Receives uploaded media from the frontend.
- Stores uploaded files.
- Creates backend-controlled asset information.
- Extracts available media capture timestamps.

#### Asset Loader

The `AssetLoader` validates uploaded media and extracts technical metadata using FFprobe.

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

#### AI Planning

The AI prompt engine interprets the user's instructions and can return an asset order based on the requested arrangement.

For example:

> "Put number 2 first, number 1 second, and number 3 last."

The AI can return the corresponding asset IDs in the requested order.

#### Timeline

The planner converts the AI-generated plan into a timeline containing the selected assets and their order.

#### Render Plan

A render plan is generated from the timeline and passed to the renderer.

#### FFmpeg Renderer

The FFmpeg renderer currently:

- Accepts a render plan.
- Reads assets from the timeline.
- Handles image inputs.
- Scales media to a vertical `720x1280` format.
- Preserves aspect ratio.
- Adds padding when necessary.
- Assigns image durations.
- Concatenates the assets.
- Encodes the final video using H.264.
- Produces an MP4 file.

The current prototype has successfully rendered a multi-image highlight video.

---

## Current Architecture

The backend separates upload handling, asset processing, AI planning, timeline creation, composition, and rendering.

```text
Frontend
   |
   v
Create Video Request
   |
   v
Backend Upload Handling
   |
   v
File Validation and Saving
   |
   v
Initial Asset Records
   |
   v
Background Video Job
   |
   v
Video Orchestrator
   |
   v
AssetLoader
   |
   v
Media Analysis / AI Planning
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
Composer
   |
   v
Render Plan
   |
   v
FFmpeg Renderer
   |
   v
Generated MP4
   |
   v
Job Result
   |
   v
Frontend Preview / Download
```

### Main Components

| Component | Responsibility |
|---|---|
| Frontend | Collects media and user instructions |
| Backend | Handles uploads, requests, and background jobs |
| AssetLoader | Validates media and extracts technical metadata |
| AI Planning | Interprets user instructions and produces an asset plan |
| Planner | Converts the plan into a timeline |
| Composer | Produces the render plan |
| FFmpeg Renderer | Generates the final MP4 video |
| Job Manager | Tracks generation status and results |

---

## Current Development Priorities

The next stage focuses on reliability and improving the existing system before introducing additional features.

Areas requiring continued review and testing include:

- Upload validation and error handling.
- Corrupted and unsupported media handling.
- Metadata extraction reliability.
- AI provider failures and malformed responses.
- Asset ordering and timeline validation.
- FFmpeg rendering errors and output verification.
- Background job failure handling.
- Storage management and cleanup.
- Frontend progress tracking and download reliability.
- Testing with different media types and file sizes.

---

## Planned Development Direction

1. Audit the existing backend architecture.
2. Improve upload and asset validation.
3. Strengthen AI response validation and error handling.
4. Improve timeline and render-plan reliability.
5. Test FFmpeg output quality and compatibility.
6. Improve background job management.
7. Integrate Cloudflare R2 for media storage.
8. Develop more advanced scene and highlight detection.
9. Evaluate audio intelligence and transcription.
10. Prepare the application for broader use and future scalability.

---

## Development Approach

Impact Reels is being developed incrementally, with an emphasis on preserving working functionality and improving reliability before expanding capabilities.

**Inspect → Understand → Improve → Test → Repeat.**
