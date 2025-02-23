// /api/quiz/route.js

export async function POST(request) {
  const { chatHistory } = await request.json();

  // URL for your Python FastAPI server's quiz generation endpoint
  const pythonApiQuizUrl = "http://127.0.0.1:8000/quiz";

  try {
    // Forward the chat history to the Python API
    const response = await fetch(pythonApiQuizUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
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
    console.error("Error calling Python API for quiz:", error);

    // Return a fallback error response
    return new Response(
      JSON.stringify({
        type: "quiz",
        content: `Could not reach the Python API for quiz: ${error}`
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" }
      }
    );
  }
}
