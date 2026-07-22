import requests
import json
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()


MY_EMAIL = os.environ['MY_EMAIL']
APP_PASSWORD = os.environ['APP_PASSWORD']
OpenWeather_API_KEY = os.environ['OPENWEATHER_API_KEY']


My_Parameters ={
    "lat": 53.765762,
    "lon": -2.692337,
    "appid": OpenWeather_API_KEY,

}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params = My_Parameters)
print(response.status_code)
response.raise_for_status()

data = response.json()


today = datetime.now().strftime("%Y-%m-%d")


will_rain = False

# Store rainy times
rain_times = []

for forecast in data["list"]:

    forecast_date, forecast_time = forecast["dt_txt"].split()
    hour = int(forecast_time[:2])

    # Ignore forecasts that aren't today
    if forecast_date != today:
        continue

    # Ignore forecasts outside office hours
    if not (8 <= hour <= 18):
        continue

    weather_id = forecast["weather"][0]["id"]

    #if weather_id < 700:
    if True:
        will_rain = True
        rain_times.append(forecast_time)

if will_rain:

    message = "Subject:Umbrella Reminder \n\n"
    message += "Rain is expected during office hours.\n\n"
    message += "Expected rain times:\n"

    for time in rain_times:
        message += f"- {time[:5]}\n"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()

        connection.login(
            user = MY_EMAIL
            , password = APP_PASSWORD)


        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=message
        )

    print("Email sent!")

else:
    print(" No rain expected during office hours.")





