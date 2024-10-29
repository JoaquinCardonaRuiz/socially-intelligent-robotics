import json

import numpy as np
from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (
    Dialogflow,
    DialogflowConf,
    GetIntentRequest,
    QueryResult,
    RecognitionResult,
)

import json
from openai import OpenAI
credentials = json.load(open("src/credentials.json", "r"))
client = OpenAI(api_key=credentials["openai"])


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



# the callback function
def on_dialog(message):
    if message.response:
        if message.response.recognition_result.is_final:
            print("Transcript:", message.response.recognition_result.transcript)


# connect to the robot
try:
    nao = Nao(ip="10.0.0.121")

    # load the key json file (you need to get your own keyfile.json)
    keyfile_json = json.load(open("src/dialogflow-tutorial.json"))

    # set up the config
    conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

    # initiate Dialogflow object
    dialogflow = Dialogflow(ip="localhost", conf=conf)

    # connect the output of NaoqiMicrophone as the input of DialogflowComponent
    dialogflow.connect(nao.mic)

    # register a callback function to act upon arrival of recognition_result
    dialogflow.register_callback(on_dialog)

    # Demo starts
    nao.tts.request(NaoqiTextToSpeechRequest("Hello, who are you?"))
    print(" -- Ready -- ")
    x = np.random.randint(10000)


    history=[]
    for i in range(25):
        print(" ----- Conversation turn", i)
        reply = dialogflow.request(GetIntentRequest(x))

        print(reply.intent.transcript)
        nao_response = ask_llm(reply.intent.transcript, f"You are a helpful nao robot. This is the history of the conversation {history}", temp=0.9)
        history.append({'user_message': reply.intent.transcript, 'bot_response': nao_response})
        nao.tts.request(NaoqiTextToSpeechRequest(nao_response))

        
except KeyboardInterrupt:
    print("Stop the dialogflow component.")
    dialogflow.stop()
