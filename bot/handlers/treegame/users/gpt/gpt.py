import google.generativeai as genai
from bot import messages
from bot.settings import settings

async def gpt_thinks(age, sex, ves, rost, zabol, angle):
    """Анализ сколиоза с помощью Gemini"""
    try:
        genai.configure(api_key=settings.gemini.key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Преобразуем угол в строку для безопасной вставки
        angle_str = str(angle) if angle is not None else "не определен"
        if angle_str is None:
            response = 'Отправьте другое фото'
        
        prompt = f"""
        Проанализируй данные пациента и дай краткие рекомендации по сколиозу.
        
        ДАННЫЕ ПАЦИЕНТА:
        - Возраст: {age}
        - Пол: {sex}
        - Вес: {ves} кг
        - Рост: {rost} см
        - Заболевания спины: {zabol}
        - Возможность сколиоза: {angle_str}% если больше 5 - сколиоз есть. Чем больше процент - больше степень
        
        ТРЕБОВАНИЯ К ОТВЕТУ:
        - Ответ должен быть кратким (3-5 предложений)
        - Общайся простым языком с пациентом
        - Не упоминай точные цифры угла кривизны
        - Скажи есть ли признаки сколиоза или нет
        - Если есть признаки - дай 2-3 конкретные рекомендации
        - Если признаков нет - дай 1-2 совета по профилактике
        - Учитывай возраст и вес пациента
        - Будь доброжелательным и поддерживающим
        - всегда отвечай позитивно и со смайликами
        - основывайся на его данных

        Пример хорошего ответа: 
        "На основе анализа выявлены незначительные признаки сколиоза. Рекомендую: 1) Ежедневная лечебная гимнастика 2) Консультация ортопеда 3) Контроль осанки при сидении""
        """

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