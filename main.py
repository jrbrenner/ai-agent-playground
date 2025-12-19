import os
import sys
from dotenv import load_dotenv

# 1. SETUP ENVIRONMENT
# Load secrets from the .env file
load_dotenv() 

# Verify keys are loaded (Optional safety check)
if not os.environ.get("GROQ_API_KEY"):
    print("❌ Error: GROQ_API_KEY not found in .env file.")
    sys.exit(1)

# 2. IMPORT YOUR GRAPH
# We import the compiled graph object from your src/graph.py file
from src.graph import graph

def run_chat():
    print("⚡ Groq Agent System Online")
    print("Type 'quit' or 'exit' to stop.")
    print("-" * 40)
    
    # We create a specific thread ID so the bot remembers the conversation
    config = {"configurable": {"thread_id": "main-session-1"}}

    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        # 3. RUN THE GRAPH
        # We stream 'values' to get the full message history updates
        events = graph.stream(
            {"messages": [("user", user_input)]}, 
            config=config,
            stream_mode="values"
        )

        for event in events:
            if "messages" in event and event["messages"]:
                last_msg = event["messages"][-1]
                
                # Logic to print only the Agent's response (or Tool outputs)
                if last_msg.type == "ai":
                    # Only print if there is actual text (ignoring empty tool calls)
                    if last_msg.content:
                        print(f"🤖 Agent: {last_msg.content}")
                
                elif last_msg.type == "tool":
                    # Optional: Print tool outputs if you want to debug
                    # print(f"🔧 Tool: {last_msg.content}")
                    pass

if __name__ == "__main__":
    run_chat()