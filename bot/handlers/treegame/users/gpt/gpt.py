import google.generativeai as genai
from bot import messages
from bot.settings import settings

async def gpt_thinks(age, sex, ves, rost, zabol, angle):
    """Анализ сколиоза с помощью Gemini"""
    try:
        genai.configure(api_key=settings.gemini.key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        prompt = f"""
        На основе данных тебе нужно определить степень сколиоза и вывести методики для лечения. 
        Твой ответ - сообщение что будет видеть пользователь, поэтому общайся просто и кратко, не упоминая реальный градус сколиоза.
        тебе необходимо лишь сказать есть сколиоз или нет. при наличии необходимо предположить степень и выдать рекомендации. общайся на русском.
        Данные: рост: {rost} вес: {ves} пол: {sex} заболевание: {zabol} возраст: {age} угол: {angle}"""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Произошла ошибка при анализе: {str(e)}"

async def gpt_thinks_2(message):
    """Вторая функция для общения с Gemini"""
    try:
        genai.configure(api_key=settings.gemini.key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")

        prompt = messages.gpt_promt_2.format(message=message)
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"