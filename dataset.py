import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")
api_key = api_key.strip()

printOutput = False
query = "why is the sky blue"

loop = 3
currentIteration = 0

while loop > 0:
    print(f"\n Fetching response {currentIteration}. There are {loop} response(s) left.\n" \
    "-------------------------------------------------------------------------- \n")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemma-3n-e4b-it",
            "messages": [
                {
                    "role": "user",
                    # "content": "What is the probability we will reach AGI by the end of 2027? Estimate as a percentage."
                    "content": query
                }
            ],
            "reasoning": {
                "effort": "high", 
            }
        }
    )

    # response.raise_for_status()

    data = response.json()
    output = data["choices"][0]["message"]
    CoTOutput = output.get("reasoning")
    StdOutput = output.get("content")
    OutputString = f'{{"query": "{query}", "output": "{StdOutput}"}}'

    with open('DatasetTest.json', 'a', encoding='utf-8') as json_file:
        json.dump({"query": query, "output": StdOutput}, json_file, ensure_ascii=False)
        json_file.write('\n')
    loop-= 1
    currentIteration+= 1

    if loop == 0:
        print("Synthetic dataset complete")

if printOutput:
    print("\n\n Outputting Reasoning" \
    "-------------------------------------------------------------------------- \n\n")
    time.sleep(2)
    print(CoTOutput)
    time.sleep(3)
    print(" \n\n Outputting Content" \
    "-------------------------------------------------------------------------- \n\n")
    time.sleep(2)
    print(StdOutput)