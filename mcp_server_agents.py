import asyncio
import openai
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

api_key = os.getenv("OPENAI_API_KEY")
async def main():
    model = ChatOpenAI(model="gpt-4o")
    
# Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    async with MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["/Users/Z00F6DP/Documents/Coding/myvenv/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        }
    }) as client:
        agent = create_react_agent(model, client.get_tools())
        while True:
            user_input = input("Enter your query (or type 'exit' to quit): ")
            if user_input.lower() in {"exit", "quit"}:
                print("Exiting the program.")
                break

            response = await agent.ainvoke({"messages": user_input})
            final_message = response["messages"][-1].content
            print("Agent Response:", final_message)

"""         # Example: Math query
        math_response = await agent.ainvoke({"messages": "What's (7 + 9) x 10?"})
        math_output = math_response["messages"][-1].content
        print("Math Response:", math_output)
        
        # Example: Weather query
        weather_response = await agent.ainvoke({"messages": "What's the weather in London?"})
        weather_output = weather_response["messages"][-1].content
        print("Weather Response:", weather_output) """

if __name__ == "__main__":
    asyncio.run(main())
