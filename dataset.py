import requests
import json
import time
import csv

printOutput = False

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    },
    json={
        "model": "google/gemma-3n-e4b-it:free",
        "messages": [
            {
                "role": "user",
                # "content": "What is the probability we will reach AGI by the end of 2027? Estimate as a percentage."
                "content": "hey"
            }
        ],
        "reasoning": {
            "effort": "high", 
        }
    }
)


data = response.json()
output = data["choices"][0]["message"]
CoTOutput = output.get("reasoning")
StdOutput = output.get("content")

with open('DatasetTest.json', 'w', newline='', encoding='utf-8') as json_file:
    writer = csv.writer(json_file)
    writer.writerow([StdOutput]) 

if printOutput:
    print("\n\n Outputting reasoning" \
    "-------------------------------------------------------------------------- \n\n")
    time.sleep(2)
    print(CoTOutput)
    time.sleep(3.6)
    print(" \n\n Outputting Content" \
    "-------------------------------------------------------------------------- \n\n")
    time.sleep(2)
    print(StdOutput)