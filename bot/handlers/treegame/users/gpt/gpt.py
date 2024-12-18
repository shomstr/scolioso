import google.generativeai as genai
from bot import messages
from bot.settings import settings

async def gpt_thinks(message):
    genai.configure(api_key=settings.gemini.key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = messages.gpt_promt.format(message=message)

    response = model.generate_content(prompt)
    return response.text

async def gpt_thinks_2(message):
    genai.configure(api_key=settings.gemini.key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = messages.gpt_promt_2.format(message=message)

    response = model.generate_content(prompt)
    return response.text

