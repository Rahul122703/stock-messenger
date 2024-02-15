import requests
import datetime as dt
import smtplib
import math

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_APIKEY = "1PXK9VZ4FIFQYY3B"
NEWS_APIKEY = "00f92c7b0cfc44f989187c547fa0f453"

MY_EMAIL = "killbusyness@gmail.com"
RECIVER_EMAIL = "killkamam3@gmail.com"
app_password = "pgvm ritu mjxi ybmj"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameter = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": f"{60}min",
    "apikey": STOCK_APIKEY,
}
today_day = dt.datetime.now()
stock_api = requests.get(url="https://www.alphavantage.co/query?", params=stock_parameter)
stock_api.raise_for_status()

key_yesterday = f"{today_day.year}-{today_day.month}-{today_day.day-2} 19:00:00"
key_daybeforeYes = f"{today_day.year}-{today_day.month}-{today_day.day-3} 19:00:00"

yesterday_data = float(stock_api.json()['Time Series (60min)'][key_yesterday]['2. high'])
day_before_yesterday_data = float(stock_api.json()['Time Series (60min)'][key_daybeforeYes]['2. high'])
percentage_num = (((yesterday_data - day_before_yesterday_data)/day_before_yesterday_data)*100)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_parameter = {
    "q": "tesla",
    "apikey": NEWS_APIKEY,
}
news_api = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameter)
news_msg = news_api.json()['articles']
three_articles = news_msg[:3]
def remove_ascii(string):
    new_string = ""
    for char in string:
        if (ord(char) >= 65) and (ord(char) <= 122) or (char == " "):
            new_string += char
    return new_string


formatted = [f"{remove_ascii(article['title'])}\nBRIEF: {remove_ascii(article['description'])}" for article in three_articles]

if percentage_num < 5 or percentage_num > 5:
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=MY_EMAIL, password=app_password)
    for article in formatted:
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIVER_EMAIL, msg=f"STOCK:{math.ceil(percentage_num)}% \n{article}")
    connection.close()



