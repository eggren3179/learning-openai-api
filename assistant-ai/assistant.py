import openai
import os
import sys
from dotenv import load_dotenv
import numpy as np
import logging
import time
import json

#ログレベルの設定
logging.basicConfig(stream=sys.stdout, level=logging.INFO, force=True)

#環境変数からOpenAIのAPIキー読み込み
load_dotenv(override=True)
openai.api_key = os.getenv("openai_api_key")

client = openai.OpenAI(api_key=openai.api_key)

# Assistant（Code Interpreter）の作成
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Threads
thread = client.beta.threads.create()


# Message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# run 
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Ren. The user has a premium account."
)

# 
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

i = 0 
while True:
    result_json = json.loads(run.model_dump_json(indent=2))
    print(result_json)
    i += 1
    if result_json["status"] == "completed":
        break
    if i == 10:
        break
    time.sleep(3)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print("")
print("Completed!\n")

for message in reversed(messages.data):
    print(f"{message.role}:\n {message.content[0].text.value}\n")