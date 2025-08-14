# ScAInce — your AI-powered study buddy

> ScAInce is a visual-first AI tutor that explains tough topics step-by-step, verifies formulas, and generates interactive visualizations (and animations) to make learning stick.


## ✨ Features

- Guided explanations: builds concepts from fundamentals → intermediate → advanced.
- Worked steps & rationale: shows the approach behind answers and key steps taken.
- Interactive visuals: graphs, charts, and sandboxed web code to “see” the concept.
- Animated math (optional): Manim renders short animations for math/physics topics.
- Relevant videos: embeds YouTube suggestions when visuals aren’t straightforward.
- Formula checks: uses Wolfram|Alpha to validate symbolic/math expressions.


## 🧱 How it works (architecture)

- **Frontend**: Next.js web app (chat UI + visualization canvas + YouTube embeds).
- **Agent**: LLM with a small set of tools (visualize, math-check, video-suggest, etc.).
- **Code sandbox**: when the agent returns web code (e.g., p5.js/D3/vanilla JS), it runs in an isolated iframe.
- **Math & verification**: Wolfram|Alpha API; optional local math engine.
- **Animations**: Manim (Python) can render short clips server-side and stream them to the UI.
- **Backend**: FastAPI routes requests, manages tool calls, and mediates outputs.

## Usage

### Python Server

```bash
cd python
python3 -m uvicorn app:app --reload
```

### Web App

```bash
npm install
npm run dev
```

## 🤝 Contributing

- PRs welcome! If you’re adding a new tool:
- Keep inputs/outputs minimal and typed.
- Add a small unit test and one UI example.
- Update this README and the tool registry.