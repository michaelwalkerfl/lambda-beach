import requests
import os
import smtplib
from datetime import datetime

# South Beach, Miami Beach, FL
lat = '25.782721'
lon = '-80.140556'
exclude = 'minutely,hourly,alerts'
API_key = os.getenv('WEATHER_API_KEY')

api_url = (
    f'https://api.openweathermap.org/data/3.0/onecall?' +
    f'lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}&units=imperial'
)

if os.path.isfile('.env'):
    from dotenv import load_dotenv
    load_dotenv()


def __send_notification_email(msg_body: str) -> None:
    to = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')
    mail_subject = f'Weekend Weather Forecast {datetime.today().strftime("%m/%d/%Y")}'
    mail_message = f'Subject: {mail_subject}\n\n{msg_body}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(to, password)
    server.sendmail(to, to, mail_message)
    server.close()


def handler(event, context):
    response = requests.get(api_url)
    data = response.json()
    rain = ['rain', 'thunderstorm', 'drizzle']
    # Run once on Thursday to grab weekend rain or not
    saturday = data['daily'][2]['weather'][0]['main'].lower()
    sunday = data['daily'][3]['weather'][0]['main'].lower()
    if saturday in rain:
        saturday_status = 'is raining, good time to read a book indoors.'
    else:
        saturday_status = 'is beach day!'
    if sunday in rain:
        sunday_status = 'is raining, good time to read a book indoors.'
    else:
        sunday_status = 'is beach day!'
    msg = f'Your weekend forecast: \nSaturday: {saturday_status}\nSunday: {sunday_status}.'
    __send_notification_email(msg)


handler(None, None)
