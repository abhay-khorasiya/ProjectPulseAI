const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";


async function request(
  url,
  options = {}
) {
  const response = await fetch(
    `${API_BASE_URL}${url}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },

      ...options,
    }
  );

  if (!response.ok) {
    let message =
      "Something went wrong.";

    try {
      const errorData =
        await response.json();

      message =
        errorData.detail ||
        errorData.message ||
        message;
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}


export async function analyzeAndSaveConversation(
  source,
  text
) {
  return request(
    "/api/analyze-and-save",
    {
      method: "POST",

      body: JSON.stringify({
        source,
        text,
      }),
    }
  );
}


export async function getProjectMemory() {
  return request(
    "/api/memory"
  );
}


export async function searchProjectMemory(
  query
) {
  return request(
    `/api/memory/search?q=${encodeURIComponent(
      query
    )}`
  );
}


export async function getDashboardStats() {
  return request(
    "/api/memory/stats"
  );
}


export async function updateMemoryStatus(
  itemId,
  status
) {
  return request(
    `/api/memory/${itemId}/status`,
    {
      method: "PATCH",

      body: JSON.stringify({
        status,
      }),
    }
  );
}