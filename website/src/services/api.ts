export const API_BASE_url = process.env.NODE_ENV === "production"
  ? "/api/v1"
  : "http://localhost:8000/api/v1";

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface SourceReference {
  source_file: string;
  header_path?: string;
  snippet: string;
  score: number;
}

export interface ChatRequest {
  query: string;
  selected_text?: string;
  history: ChatMessage[];
}

export async function sendChatRequest(
  request: ChatRequest,
  onToken: (token: string) => void,
  onSources: (sources: SourceReference[]) => void,
  onError: (error: string) => void,
  onComplete: () => void
) {
  try {
    const response = await fetch(`${API_BASE_url}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    if (!response.body) return;

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.slice(6);
          if (dataStr === "[DONE]") {
            onComplete();
            return;
          }
          try {
            const parsed = JSON.parse(dataStr);
            if (parsed.type === "token") {
              onToken(parsed.data);
            } else if (parsed.type === "sources") {
              onSources(parsed.data);
            }
          } catch (e) {
            console.error("Failed to parse SSE data", e);
          }
        }
      }
    }
  } catch (err) {
    onError(String(err));
  }
}
