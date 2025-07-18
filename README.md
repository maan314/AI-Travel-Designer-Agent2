🌍 AI Travel Designer Agent
A conversational multi-agent travel assistant built with Chainlit, OpenAI Agent SDK, Gemini API, designed to simulate personalized travel planning experiences.

✈️ What It Does
The AI Travel Designer Agent helps users plan dream vacations by dynamically handing off tasks to specialized sub-agents, each simulating parts of the travel experience.

🤖 Agent Flow & Capabilities
🔀 Multi-Agent Orchestration using OpenAI Agent SDK:

📍 DestinationAgent: Recommends travel locations based on user interests

🛏️ BookingAgent: Simulates flight and hotel bookings

🍽️ ExploreAgent: Suggests local attractions and food experiences

🧰 Tool Support:

get_flights() – Simulates flight results with mock data

suggest_hotels() – Returns hotel recommendations using mock data

🧠 Gemini API Integration: Enriches destination suggestions and reasoning-based responses

🪄 Chainlit UI: Enables real-time user interaction in a chatbot-style experience

🔧 Tech Stack
OpenAI Agent SDK + Runner

Chainlit – Chat interface

Gemini API – Contextual suggestions & creative planning

Python Tools with Mock Data

🌐 Example Use Case
User: I want a beach vacation in July.
DestinationAgent: How about Bali or the Maldives for perfect beach vibes?
Handoff → BookingAgent
BookingAgent: Here are available flights and hotels.
Handoff → ExploreAgent
ExploreAgent: You should check out snorkeling at Blue Lagoon and try local seafood at Jimbaran Bay.