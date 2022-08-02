from locale import currency
import requests
from bs4 import BeautifulSoup
import time
import smtplib

class Currency:
    Spirit_Airlines_Inc = 'https://www.google.com/finance/quote/SAVE:NYSE?window=6M'#сайт
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.802 Yowser/2.5 Safari/537.36'}
    #my user agent я не бот
    
    current_converted_price = 0
    difference = 0.02
    
    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace("$", " "))
    
    def get_currency_price (self):#текущая цена акции
        full_page = requests.get (self.Spirit_Airlines_Inc, headers=self.headers)
        soup = BeautifulSoup (full_page.content, 'html.parser')
        convert = soup.find_all("div", {"class": "YMlKec fxKbKc"})
        return convert[0].text #значения переменной с ценой для сравнения с будущей ценой

    def check_currency(self):   
        currency = float(self.get_currency_price().replace("$", " "))
        if currency <= self.current_converted_price - self.difference:
            print ("Цена акции упала")  
            self.send_mail()
        print ("Сейчас стоимость акции = " + str(currency))
        time.sleep(10)
        self.check_currency()
        
    def send_mail(self): #Функция для отправки сообщения на почту
        server = smtplib.SMTP("smtp.mail.ru", 465)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        server.login ('hitman-dimas@mail.ru', 'm8xh2tWKXigeDwikgQUp')
        
        subject = 'Price'
        body = 'Price is down'
        message = f'Suject: {subject}\n\n{body}'
        
        server.sendmail(
            'admin@itproper.com',
            'hitman-dimas@mail.ru',
            message
        )
        server.quit()
        
        
currency = Currency ()#объект на основе класса
currency.check_currency()

