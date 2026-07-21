import { Composition } from "remotion";
import { HighlightVideo } from "./Video";
import data from "../public/data.json";

export const RemotionRoot = () => {
  const totalDuration =
    data.clips.reduce((sum, clip) => sum + clip.duration, 0) * 30;

  return (
    <Composition
      id="HighlightVideo"
      component={HighlightVideo}
      durationInFrames={totalDuration}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        clips: data.clips,
        music: data.music,
      }}
    />
  );
};