from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import (
    NaoqiTextToSpeechRequest,
)
import json
from openai import OpenAI
credentials = json.load(open("src/credentials.json", "r"))
client = OpenAI(api_key=credentials["openai"])



nao = Nao(ip="10.0.0.121")  # adjust this to the IP adress of your robot.

def ask_llm(query_text, system_prompt, temp=1.1):
    # Fetch a response from the LLM
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_text},
        ],
        temperature=temp
    )
    return completion.choices[0].message.content

while True:
    message = input("Ask something: ")
    nao.tts.request(NaoqiTextToSpeechRequest(ask_llm(message, "You are a helpful nao robot.", temp=0.9)))
    