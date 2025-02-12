import os
import datetime
import time
import threading
from agent import Agent
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

AGENT_NAME = os.getenv("AGENT_NAME", "my-agent")
TIME_FILE = 'TIME_FILE.txt'

# Initialize initial_time from TIME_FILE or fallback to current time
if os.path.exists(TIME_FILE):
    with open(TIME_FILE, 'r') as f:
        datetime_str = f.read().strip()
    try:
        initial_time = datetime.datetime.fromisoformat(datetime_str)
    except Exception:
        initial_time = datetime.datetime.now()
else:
    initial_time = datetime.datetime.now()

table_name = AGENT_NAME
agent = Agent(initial_time=initial_time, table_name=table_name)
agent.update_time()

# Use agent to think the current date and time
last_interaction_time = datetime.datetime.now()
agent.think(f"The current date and time is {last_interaction_time.strftime('%Y-%m-%d %H:%M:%S')}")

print(f"Hello, I'm Xan. How's tricks?")

input_received = False
stop_timer_thread = False

def read_time_periodically():
    global stop_timer_thread
    while not stop_timer_thread:
        agent.update_time()
        for _ in range(300):  # sleeps for 300 seconds (5 minutes)
            if not stop_timer_thread:
                time.sleep(1)
            else:
                break

def check_for_input():
    global stop_timer_thread
    while True:
        userInput = input('Input to AI: ')
        if userInput.lower() == "farewell":
            response = agent.action(userInput)
            print(response, "\n")
            stop_timer_thread = True  # stop the timer thread
            time.sleep(5)  # wait for 5 seconds to allow for graceful exit
            exit(0)  # gracefully terminate the program
        elif userInput.lower().startswith("read:"):
            agent.read(" ".join(userInput.split(" ")[1:]))
        elif userInput.lower().startswith("think:"):
            agent.think(" ".join(userInput.split(" ")[1:]))
        else:
            agent.update_time()  # Update time before responding
            response = agent.action(userInput)
            print(response, "\n")

# Create and start the threads
timer_thread = threading.Thread(target=read_time_periodically)
input_thread = threading.Thread(target=check_for_input)
timer_thread.start()
input_thread.start()

# Wait for both threads to finish
timer_thread.join()
input_thread.join()

print("Talk to the AI!")

while True:
    userInput = input()
    if userInput:
        if userInput.startswith("read:"):
            agent.read(" ".join(userInput.split(" ")[1:]))
            print("Understood! The information is stored in my memory.")
        elif userInput.startswith("think:"):
            agent.think(" ".join(userInput.split(" ")[1:]))
            print("Understood! I stored that thought into my memory.")
        elif userInput.startswith("readDoc:"):
            agent.readDoc(" ".join(userInput.split(" ")[1:]))
            print("Understood! I stored the document into my memory.")
        else:
            response = agent.action(userInput)
            print(response)
            with open(TIME_FILE, 'r') as f:
                datetime_str = f.read().strip()  # read from file and remove any whitespace
    else:
        print("SYSTEM - Give a valid input")
