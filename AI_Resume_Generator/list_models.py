from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

models = client.models.list()

for model in models.data:
    print(model.id)