export async function createHighlightRequest(
  files,
  prompt,
  fetchImpl = fetch,
  endpoint
) {
  const API_URL =
    endpoint ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://127.0.0.1:8000";

  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  formData.append("prompt", prompt);

  return fetchImpl(`${API_URL}/create-highlight`, {
    method: "POST",
    body: formData,
  });
}