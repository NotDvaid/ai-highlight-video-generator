import subprocess
from service.renderer.timeline import Timeline
from uuid import uuid4
from pathlib import Path

    # Responsibilities:
    #
    # 1. Receive Timeline.
    # 2. Read each Asset from the Timeline.
    # 3. Build an FFmpeg command.
    # 4. Run FFmpeg.
    # 5. Verify rendering succeeded.
    # 6. Return the output path.

class FFmpegRenderer:
    def render(self, timeline: Timeline):
        cmd = ["ffmpeg"]
        filename = str(uuid4())+ ".mp4"
        output_folder = Path("service/storage")
        for asset in timeline.assets:
            cmd.extend(["-i",asset.path])
        final_output = output_folder/filename 
        cmd.extend(["-c:v","libx264" , "-pix_fmt", "yuv420p",final_output])
        subprocess.run(cmd)





            