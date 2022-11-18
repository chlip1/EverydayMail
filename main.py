import smtplib
from datetime import date
import requests
import random
import json

MY_EMAIL = '#'
PASSWORD = '#'
WEATHER_BASE = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_FORECAST = 'http://api.openweathermap.org/data/2.5/forecast?'
WEATHER_KEY = '#'
PM_URL = "https://api.openaq.org/v1/measurements?location=10770&parameter=pm25"
NAME1 = "#"
NAME2 = "#"
MAIL1 = '#'
MAIL2 = "#"

class Email():
    def __init__(self, name, mail_adr) -> None:
        self.today = date.today()
        self.day = self.today.strftime("%d")
        self.connection = smtplib.SMTP('smtp.gmail.com')
        self.name = name
        self.mail_adr = mail_adr
        self.getWeather()
        self.getPM()
        self.getQuote()
        self.getGreatings()
        self.forecastWeather()
        self.createMessage()
        self.sendMailToYou()
        print(self.msg)

    def getWeather(self):
      url = WEATHER_BASE + 'appid=' + WEATHER_KEY + '&q=Gdansk'
      response = requests.get(url)
      data = response.json()
      for i in data['weather']: self.weather = i['description']
      self.temp = round(list(data['main'].values())[1] - 273, 1)
      self.pressure = list(data['main'].values())[4]
      self.wind_speed = list(data['wind'].values())[0]
      self.clouds = list(data['clouds'].values())[0]

    def getQuote(self):
        with open('quotes.json', 'r', errors='ignore') as file:
            data = json.load(file)
            choosen_line = random.choice(data["quotes"])
            self.quote = choosen_line["quote"]
            self.author = choosen_line["author"]
    
    def getGreatings(self):
        with open('greatings.json', 'r', errors='ignore') as file:
            all_greatings = file.readlines()
            self.greatings = random.choice(all_greatings)

    def getPM(self):
        data = requests.get(PM_URL).json()
        data = data["results"][0]
        self.pm = data['value']

    def forecastWeather(self):
        url = WEATHER_FORECAST + 'appid=' + WEATHER_KEY + '&q=Gdansk'
        print(url)
        data = requests.get(url).json()
        data = data["list"]

        for line in data: 
            if line['dt_txt'].endswith('12:00:00'):
                self.temp_12 = round(line['main']['temp'] - 273, 1)
            if line['dt_txt'].endswith('15:00:00'):
                self.temp_15 = round(line['main']['temp'] - 273, 1)
            if line['dt_txt'].endswith('18:00:00'):
                self.temp_18 = round(line['main']['temp'] - 273, 1)

    def createMessage(self):
        self.msg = f"""Subject:Everyday mail {self.today}:)\n
        {self.greatings.strip()[1:-2]}, {self.name}

        {self.quote}
        ~{self.author}

        6:30...

        Weather: {self.weather.capitalize()}, 
        Temperature: {self.temp}C,
        Pressure: {self.pressure} hPa,
        Wind speed: {self.wind_speed}km/h,
        Clouds: {self.clouds}%,
        PM: {self.pm} microg/m3

        Today's weather:

        12:00 - {self.temp_12}C
        15:00 - {self.temp_15}C
        18:00 - {self.temp_18}C

        Lov u"""
   
    def sendMailToYou(self):
        self.connection.starttls()
        self.connection.login(user=MY_EMAIL, password=PASSWORD)
        self.connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=self.mail_adr,
            msg=self.msg
        )
        self.connection.close()


if __name__ == '__main__':
    Email(NAME1, MAIL1)
    Email(NAME2, MAIL2)
