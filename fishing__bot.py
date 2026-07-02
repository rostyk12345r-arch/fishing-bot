import requests

# --- НАЛАШТУВАННЯ ---
TOKEN = "8647008579:AAHEYCKB6fOGILPR2AOXGkVxP_e5tRmEDu0"
CHAT_ID = "5950691116"
LAT = 49.84   # Широта (Львів)
LON = 24.03   # Довгота

def get_weather_and_fishing():
    # Запит до безкоштовного API погоди
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,weather_code,pressure_msl&timezone=auto"
    response = requests.get(url).json()

    current = response['current']
    temp = current['temperature_2m']
    pressure_hpa = current['pressure_msl']
    code = current['weather_code']

    # Переведення тиску в мм рт. ст.
    pressure_mm = round(pressure_hpa * 0.750062)

    # Визначення стану погоди за кодом
    weather_desc = "Мінлива хмарність"
    if code == 0: weather_desc = "Ясно, безхмарно ☀️"
    elif code in [1, 2, 3]: weather_desc = "Мінлива хмарність ⛅️"
    elif code in [51, 53, 55, 61, 63, 65]: weather_desc = "Йде дощ 🌧️"
    elif code in [71, 73, 75, 85, 86]: weather_desc = "Сніг ❄️"

    # Алгоритм прогнозу клювання
    bite_score = 3  # Середній базовий рівень (від 1 до 5)

    # Вплив тиску
    if 755 <= pressure_mm <= 765:
        bite_score += 1  # Ідеальний тиск
    elif pressure_mm < 748 or pressure_mm > 770:
        bite_score -= 2  # Риба в'яла через аномальний тиск

    # Вплив опадів
    if code in [61, 63]:  # Легкий дощ
        bite_score += 1

    bite_score = max(1, min(5, bite_score))

    bite_forecasts = {
        1: "Клювання майже відсутнє ❌ Риба ховається і не реагує.",
        2: "Слабкий кльов 🎣 Доведеться дуже постаратися.",
        3: "Середній кльов 🐟 Риба активна, але перебирає харчами.",
        4: "Гарний кльов! 🦈 Можна сміливо збирати снасті.",
        5: "Шалений кльов! 🔥 Риба бере на все підряд!"
    }

    # Поради щодо наживки
    if temp > 15:
        bait_advice = "🌽 Рослинні: кукурудза, мастирка, перловка, горох. З тваринних — опариш."
    else:
        bait_advice = "🪱 Тваринні: червоний черв'як, мотиль, опариш. Для хижака — силікон або блешня."

    # Формування повідомлення з вашим особливим вітанням
    text = (
        f"Доброго ранку Король👑Ростислав Васильович\n\n"
        f"📅 *Прогноз погоди та риболовлі на сьогодні:*\n\n"
        f"🌡️ *Температура:* {temp}°C\n"
        f"☁️ *Погода:* {weather_desc}\n"
        f"🧭 *Атмосферний тиск:* {pressure_mm} мм рт. ст.\n\n"
        f"🎣 *Прогноз клювання:* {bite_forecasts[bite_score]}\n"
        f"💼 *На що ловити:* {bait_advice}"
    )

    return text

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    message = get_weather_and_fishing()
    send_telegram(message)