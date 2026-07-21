import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Video,
  Audio,
  useVideoConfig,
} from "remotion";

/* -------------------- TYPES -------------------- */

type Clip = {
  src: string;
  start: number;     // seconds
  duration: number;  // seconds
  caption?: string;
};

type Music = {
  src: string;
};

type Props = {
  clips: Clip[];
  music?: Music;
};


import {
  useCurrentFrame,
  interpolate,
} from "remotion";

const CinematicVideo: React.FC<{
  src: string;
  startFrom: number;
  durationInFrames: number;
  transitionFrames: number;
}> = ({ src, startFrom, durationInFrames, transitionFrames }) => {
  const frame = useCurrentFrame();

  const scale = interpolate(
    frame,
    [0, durationInFrames],
    [1, 1.08],
    { extrapolateRight: "clamp" }
  );

  const opacity = interpolate(
    frame,
    [
      0,
      transitionFrames,
      durationInFrames - transitionFrames,
      durationInFrames,
    ],
    [0, 1, 1, 0],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        transform: `scale(${scale})`,
        opacity,
      }}
    >
      <Video
        src={src}
        startFrom={startFrom}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
    </AbsoluteFill>
  );
};


/* -------------------- COMPONENT -------------------- */

export const HighlightVideo: React.FC<Props> = ({ clips, music }) => {
  const { fps } = useVideoConfig();
  let currentFrame = 0;
  const TRANSITION_FRAMES = Math.floor(fps * 0.5); // 0.5 sec crossfade

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Background Music */}
      {music?.src && <Audio src={music.src} />}

      {/* Clips */}
      {clips.map((clip: Clip, i: number) => {
        const durationInFrames = Math.floor(clip.duration * fps);
        const startFromFrame = Math.floor(clip.start * fps);

        const sequence = (
          <Sequence
            key={i}
            from={currentFrame}
            durationInFrames={durationInFrames}
          >
            <AbsoluteFill
              style={{
                overflow: "hidden",
            }}
          >
            <CinematicVideo
              src={clip.src}
              startFrom={startFromFrame}
              durationInFrames={durationInFrames}
              transitionFrames={TRANSITION_FRAMES}
            />

              {/* Caption */}
              {clip.caption && (
                <div
                  style={{
                    position: "absolute",
                    bottom: 80,
                    width: "100%",
                    textAlign: "center",
                    color: "white",
                    fontSize: 42,
                    fontWeight: "bold",
                    textShadow: "0px 0px 12px rgba(0,0,0,0.8)",
                    padding: "0 40px",
                  }}
                >
                  {clip.caption}
                </div>
              )}
            </AbsoluteFill>
          </Sequence>
        );

        currentFrame += durationInFrames - TRANSITION_FRAMES;
        return sequence;
      })}
    </AbsoluteFill>
  );
};