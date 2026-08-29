import subprocess
from service.models.render_plan import RenderPlan
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
    def render(self, render_plan: RenderPlan):
        cmd = ["ffmpeg"]
        filename = str(uuid4())+ ".mp4"
        filter_inputs = []
        normalize = []
        filter_outputs = []
        output_folder = Path("service/storage")
        for i, asset in enumerate(render_plan.timeline.assets):
            filter_inputs.append(f"[{i}:v]")
            filter_results = filter_inputs[i] + "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1" + f"[v{i}]"
            normalize.append(filter_results)
            filter_outputs.append(f"[v{i}]")
            if asset.media_type == "image":
                cmd.extend(["-loop", "1", "-t",str(asset.duration), "-i",asset.path])
                print("Processing image:", asset.path)
            else:
                  cmd.extend(["-i",asset.path])
        filter_graph = ";".join(normalize)
        filter_outputs_graph = "".join(filter_outputs)
        
        cmd.extend(["-filter_complex",f"{filter_graph};{filter_outputs_graph}concat=n={len(normalize)}:v=1"])
        final_output = output_folder/filename 
        cmd.extend(["-c:v","libx264" , "-pix_fmt", "yuv420p",final_output])
        
        print(cmd)

        subprocess.run(cmd, check=True)

        return str(final_output)
        


            