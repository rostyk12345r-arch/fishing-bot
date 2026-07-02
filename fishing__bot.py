import requests

TOKEN = "8647008579:AAHEYCKB6fOGILPR2AOXGkVxP_e5tRmEDu0"
CHAT_ID_ROSTYSLAV = "5950691116"
CHAT_ID_VASYL = "627612012"

bite_forecasts = {
    1: "Клювання майже відсутнє 🚫 Риба ховається.",
    2: "Слабкий кльов 📉 Доведеться постаратися.",
    3: "Середній кльов ⚖️ Риба активна, але перебирає.",
    4: "Гарний кльов 📈 Можна сміливо збирати снасті.",
    5: "Шалений кльов 🚀 Риба бере на все підряд!"
}

def get_weather_and_fishing(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,pressure_msl"
    try:
        response = requests.get(url).json()
        current = response['current']
        temp = current['temperature_2m']
        pressure_hpa = current['pressure_msl']
        # Переводимо гектопаскалі в мм рт. ст.
        pressure_mm = round(pressure_hpa * 0.750062)
        code = current['weather_code']
        
        # Визначаємо хмарність та погоду
        if code == 0:
            weather_desc = "Ясно, безхмарно ☀️"
        elif code in [1, 2, 3]:
            weather_desc = "Мінлива хмарність ☁️"
        elif code in [51, 53, 55, 61, 63, 65]:
            weather_desc = "Йде дощ 🌧️ (хмарно)"
        elif code in [71, 73, 75, 85, 86]:
            weather_desc = "Сніг ❄️ (хмарно)"
        else:
            weather_desc = "Хмарно ☁️"

        # Прогноз клювання та вибір снасті залежно від температури
        if temp > 15:
            bite_score = 4
            bait_advice = "Рослинні: кукурудза, мастирка, перловка. З тваринних – опариш."
            rod_advice = "Краще підійде кормушка (фідер) на мирну рибу."
        elif temp > 5:
            bite_score = 3
            bait_advice = "Тваринні: червоний черв'як, мотиль, опариш. Для хижака – блешня або силікон."
            rod_advice = "Універсальний час: можна пробувати і кормушку, і спінінг."
        else:
            bite_score = 2
            bait_advice = "Тваринні наживки (мотиль) або штучні приманки на хижака."
            rod_advice = "Краще взяти спінінг, хижак зараз активніший за мирну рибу."
            
        return temp, weather_desc, pressure_mm, bite_score, bait_advice, rod_advice
    
    except Exception as e:
        print(f"Помилка отримання даних про погоду: {e}")
        return 0, "Невідомо", 0, 1, "Невідомо", "Невідомо"

def send_telegram(chat_id, greeting, temp, weather_desc, pressure_mm, bite_score, bait_advice, rod_advice):
    # Зверни увагу: зірочки для жирного тексту стоять парами і не ламають Markdown
    text = (
        f"{greeting}\n\n"
        f"🎣 *Прогноз погоди та риболовлі на сьогодні:*\n\n"
        f"🌡️ Температура: *{temp}°C*\n"
        f"☁️ Погода: *{weather_desc}*\n" 
        f"🌬️ Атмосферний тиск: *{pressure_mm} мм рт. ст.*\n\n"
        f"🎣 Прогноз клювання: *{bite_forecasts.get(bite_score, 'Невідомо')}*\n"
        f"🎣 Що краще брати: *{rod_advice}*\n"
        f"💪 На що ловити: *{bait_advice}*"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    response = requests.post(url, json=payload)
    
    # Вивід результату в консоль PythonAnywhere для перевірки
    if response.status_code == 200:
        print(f"✅ Повідомлення успішно відправлено на ID {chat_id}")
    else:
        print(f"❌ Помилка відправки на ID {chat_id}: {response.text}")

if __name__ == '__main__':
    print("Запуск скрипта...")
    
    # 1. Прогноз для Ростислава (Львів: широта 49.84, довгота 24.03)
    temp_lv, desc_lv, pres_lv, bite_lv, bait_lv, rod_lv = get_weather_and_fishing(49.84, 24.03)
    greeting_rostyslav = "Доброго ранку, король 🤴 Ростислав Васильович"
    send_telegram(CHAT_ID_ROSTYSLAV, greeting_rostyslav, temp_lv, desc_lv, pres_lv, bite_lv, bait_lv, rod_lv)
    
    # 2. Прогноз для Василя (Дуррес, Албанія: широта 41.32, довгота 19.45)
    temp_dr, desc_dr, pres_dr, bite_dr, bait_dr, rod_dr = get_weather_and_fishing(41.32, 19.45)
    greeting_vasyl = "Доброго дня, пане король 🤴 Василь Михайлович"
    send_telegram(CHAT_ID_VASYL, greeting_vasyl, temp_dr, desc_dr, pres_dr, bite_dr, bait_dr, rod_dr)
    
    print("Скрипт завершив роботу.")
