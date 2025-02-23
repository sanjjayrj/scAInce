export async function POST(request) {
  const { chatHistory, prompt } = await request.json();

  // Debug: Log the chat history
  // console.log("Chat History Received:", chatHistory);

  // URL for your Python FastAPI server
  const pythonApiUrl = "http://127.0.0.1:8000/chat";

  try {
    // Forward the request to the Python API
    const response = await fetch(pythonApiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        chat_history: chatHistory
      })
    });
    
    // Parse JSON from Python service
    const data = await response.json();
    
    // Return the Python API's JSON response to the client
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });

  } catch (error) {
    console.error("Error calling Python API:", error);

    // Return a fallback error response
    return new Response(
      JSON.stringify({
        type: "text",
        content: `Could not reach the Python API: ${error}`
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" }
      }
    );
  }
}
