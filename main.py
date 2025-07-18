from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def get_flights(from_city: str, to_city: str, date: str) -> list:
    """
    Returns a list of mock flight options from from_city to to_city on the given date.
    """
    mock_flights = [
        {
            "airline": "PakAir",
            "flight_number": "MA123",
            "from": from_city,
            "to": to_city,
            "date": date,
            "departure": "08:00 AM",
            "arrival": "11:00 AM",
            "duration": "3h",
            "price": "$199"
        },
        {
            "airline": "TenthJet",
            "flight_number": "TJ456",
            "from": from_city,
            "to": to_city,
            "date": date,
            "departure": "01:00 PM",
            "arrival": "04:00 PM",
            "duration": "3h",
            "price": "$210"
        },
        {
            "airline": "DemFly",
            "flight_number": "DF789",
            "from": from_city,
            "to": to_city,
            "date": date,
            "departure": "06:00 PM",
            "arrival": "09:00 PM",
            "duration": "3h",
            "price": "$180"
        }
    ]
    return mock_flights
@function_tool
def suggest_hotels(destination: str, check_in: str, check_out: str) -> list:
    """
    Returns a list of mock hotel suggestions in a given destination.
    """
    return [
        {
            "name": "Hotel MockStay",
            "location": f"Downtown {destination}",
            "check_in": check_in,
            "check_out": check_out,
            "price_per_night": "$120",
            "rating": 4.5,
            "amenities": ["Free WiFi", "Breakfast", "Pool"]
        },
        {
            "name": "TestInn",
            "location": f"Central {destination}",
            "check_in": check_in,
            "check_out": check_out,
            "price_per_night": "$95",
            "rating": 4.2,
            "amenities": ["WiFi", "Gym Access"]
        },
        {
            "name": "DemoSuites",
            "location": f"Near Airport, {destination}",
            "check_in": check_in,
            "check_out": check_out,
            "price_per_night": "$135",
            "rating": 4.7,
            "amenities": ["Airport Shuttle", "Free Parking"]
        }
    ]

destination_agent = Agent(
    name= "Destination Agent ",
    instructions="you are a Destination agent. You will help users with finds places for best destinations.",
)

booking_agent = Agent(
    name= "Booking Agent",
    instructions="you are a Booking agent. You will help users with booking hotels, flights, and other travel arrangements.",
)

explore_agent = Agent(
    name= "Explore Agent",
    instructions="you suggests attractions & food options for users.",
)

travel_designer_agent = Agent(
    tools=[get_flights, suggest_hotels],
    name= "Travel Designer Agent",
    instructions="you are a Travel Designer Agent that helps users design their travel plans.",
    handoffs=[destination_agent, booking_agent, explore_agent]
)

# decorator
@cl.on_chat_start
async def handle_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Welcome to the AI Travel Designer Agent, I will help you to design your travel plans.").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})

    mesg = cl.Message(content="")
    await mesg.send()

    result = Runner.run_streamed(
        travel_designer_agent,
        input=history,
        run_config=config
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await mesg.stream_token(event.data.delta)
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)