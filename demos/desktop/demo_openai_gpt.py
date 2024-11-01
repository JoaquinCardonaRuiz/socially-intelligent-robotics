from sic_framework.services.openai_gpt.gpt import GPT, GPTConf, GPTRequest, GPTResponse

"""

This demo shows how to use the OpenAI GPT model to get responses to user input,
and a secret API key is required to run it

IMPORTANT
OpenAI gpt service needs to be running:

1. pip install social-interaction-cloud[openai-gpt]
2. run-gpt

"""

# Read OpenAI key from file
with open("openai_key", "rb") as f:
    openai_key = f.read()
    openai_key = openai_key.decode("utf-8").strip()

# Setup GPT
conf = GPTConf(openai_key=openai_key)
gpt = GPT(conf=conf)


# Constants
NUM_TURNS = 5
i = 0
context = []

# Continuous conversation with GPT
while i < NUM_TURNS:
    # Ask for user input
    inp = input("Start typing...\n-->" if i == 0 else "-->")

    # Get reply from model
    reply = gpt.request(GPTRequest(inp, context_messages=context))
    print(reply.response, "\n", sep="")

    # Add user input to context messages for the model (this allows for conversations)
    context.append(inp)
    i += 1
