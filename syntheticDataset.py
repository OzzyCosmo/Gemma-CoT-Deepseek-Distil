import requests
import json
import time
import os
from dotenv import load_dotenv
import random
from random import randrange

domains = [
    "debugging a complex Python asyncio race condition",
    "a philosophical debate about utilitarianism vs deontology",
    "estimating the number of piano tuners in Chicago (Fermi problem)",
    "writing a short story where every word starts with 'S'",
    "calculating the trajectory of a rocket with changing mass",
    "analyzing the geopolitical implications of a fictional trade war",
    "a riddle about time travel paradoxes",
    "optimizing a SQL query for a massive dataset",
    "diagnosing a medical case with conflicting symptoms",
    "designing a permaculture garden for a desert climate"
    "reverse-engineering a proprietary file format without documentation",
    "drafting a legal argument for an AI-generated intellectual property dispute",
    "creating a machine-learning model that predicts solar flare intensity",
    "composing a haiku using only scientific terminology",
    "designing a decentralized governance system for a virtual nation",
    "balancing a fantasy RPG combat system for asymmetric classes",
    "modeling the spread of an invasive species using differential equations",
    "conducting a forensic analysis on a corrupted blockchain ledger",
    "prototyping a zero-waste manufacturing workflow",
    "devising a communication system for astronauts under extreme time delay",
    "reconstructing a dead language’s grammar from limited inscriptions",
    "planning a heist in a fictional world with magical constraints",
    "engineering a self-sustaining underwater research habitat",
    "debugging a distributed system suffering from clock drift",
    "writing a comedy sketch that obeys strict mathematical constraints",
    "evaluating the ethics of autonomous weapons in asymmetric warfare",
    "designing a neural interface for prosthetic limb feedback",
    "simulating the energy economy of a post-scarcity society",
    "constructing a proof for a conjecture using only combinatorial methods",
    "solving a logic puzzle involving imperfect memory and unreliable narrators"
]

length = [
    "A single sentence",
    "Two sentences",
    "Three to five sentences",
    "A paragraph",
    "A few paragraphs"
]

personas = [
    "a Ph.D. researcher being extremely precise" 
    "a confused student asking for help",        
    "a impatient software engineer",             
    "a creative writer looking for inspiration", 
    "a skeptical user trying to trick the AI",   
    "a 5-year old asking 'why'"                  
    "an overconfident amateur who thinks they already know the answer",
    "a senior professor who keeps getting sidetracked",
    "a lawyer trying to find loopholes",
    "a stoic philosopher responding in calm aphorisms",
    "a chaotic comedian who won't stay on topic",
    "a conspiracy theorist who connects unrelated ideas",
    "a poet who only speaks in fragmented metaphors",
    "a strict military officer demanding clarity",
    "a medieval alchemist interpreting everything symbolically",
    "a corporate manager obsessed with KPIs",
    "a shy beginner terrified of being wrong",
    "an AI ethics researcher overanalyzing every detail",
    "a detective grilling a suspect",
    "a tired parent who just wants a simple explanation",
    "an optimist who thinks everything is solvable",
    "a pessimist who assumes everything will fail",
    "a cryptic oracle speaking in riddles",
    "a stand-up programmer (writes code and jokes)",
    "a brutal realist who cuts straight to the point",
    "a sci-fi astronaut reporting from deep space"
]

difficulty = [
    "extremely academic and scientific",
    "child, 5 year old level",
    "high school level",
    "average person",
    "casual question"
]

load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")
api_key = api_key.strip()

printOutput = False

loop = 5
currentIteration = 0

while loop > 0:

    chosen_domain = random.choice(domains)
    output_length = random.choice(length)
    random_persona = random.choice(personas)
    random_level = random.choice(difficulty)

    # Query Generation

    print(f"\n Fetching query generation #{currentIteration}. There are {loop} query generations(s) left.")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemma-3-12b-it",
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a raw data generator. Generate exactly one user query requiring deep reasoning or chain-of-thought. The domain this question should focus on is {chosen_domain}. The length should be {output_length}. Do not include any introductory text, labels, or explanations. Do not wrap the output in quotation marks or tags. Output strictly the query body. The prompt should come from the persona of {random_persona}. The prompt difficult should be {random_level}"
                }
            ],
            "reasoning": {
                "effort": "high", 
            },
            "temperature": 1.2
        }
    )

    queryData = response.json()
    finalQueryOutput = queryData["choices"][0]["message"]["content"]
    print(finalQueryOutput)

    # Output Generation

    print(f"Fetching response {currentIteration}. There are {loop} response(s) left.\n")

    response2 = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek/deepseek-r1",
            "messages": [
                {
                    "role": "user",
                    # "content": "What is the probability we will reach AGI by the end of 2027? Estimate as a percentage."
                    "content": finalQueryOutput
                }
            ],
            "reasoning": {
                "effort": "high", 
                "exclude": False,
                "enabled": True
            }
        }
    )

    # response.raise_for_status()

    data = response2.json()
    print(data)
    output = data["choices"][0]["message"]
    CoTOutput = output.get("reasoning")
    StdOutput = output.get("content")
    OutputString = f'{{"query": "{finalQueryOutput}", "output": "{StdOutput}"}}'

    with open('DatasetTest.json', 'a', encoding='utf-8') as json_file:
        json.dump({"query": finalQueryOutput, "output": StdOutput}, json_file, ensure_ascii=False)
        json_file.write('\n')
    loop-= 1
    currentIteration+= 1

    if loop == 0:
        print("Data systhesis complete.")

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