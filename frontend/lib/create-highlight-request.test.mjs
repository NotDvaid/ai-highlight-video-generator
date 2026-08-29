import test from "node:test";
import assert from "node:assert/strict";

import { createHighlightRequest } from "./create-highlight-request.js";

test("createHighlightRequest sends FormData with media files and prompt to /create-highlight", async () => {
  const files = [
    new File(["video-bytes"], "clip.mp4", { type: "video/mp4" }),
    new File(["image-bytes"], "photo.jpg", { type: "image/jpeg" }),
  ];

  let requestUrl;
  let requestOptions;

  const fakeFetch = async (url, options) => {
    requestUrl = url;
    requestOptions = options;

    return {
      async json() {
        return { video_url: "http://example.test/highlight.mp4" };
      },
    };
  };

  const endpoint = "http://localhost:8000";

  await createHighlightRequest(files, "community fundraiser", fakeFetch, endpoint);

  assert.equal(requestUrl, `${endpoint}/create-highlight`);
  assert.equal(requestOptions.method, "POST");
  assert.ok(requestOptions.body instanceof FormData);

  const formData = requestOptions.body;
  const sentFiles = formData.getAll("files");

  assert.equal(sentFiles.length, 2);
  assert.equal(sentFiles[0].name, "clip.mp4");
  assert.equal(sentFiles[1].name, "photo.jpg");
  assert.equal(formData.get("prompt"), "community fundraiser");
});