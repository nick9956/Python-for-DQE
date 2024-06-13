from datetime import datetime
from random import choice
from os import path


class News:
    def __init__(self, text: str, city: str) -> None:
        self.text = text
        self.city = city
    
    def get_news_body(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        return '\nNews -------------------------\n{text}\n{city}, {current_time}\n'.format(
            text=self.text, city=self.city, current_time=current_time)
    
    
class PrivateAd:
    def __init__(self, text: str, expiration_date: str) -> None:
        self.text = text
        self.expiration_date = datetime.strptime(expiration_date, '%d/%m/%Y').date()

    def get_ad_body(self):
        delta = (self.expiration_date - datetime.now().date()).days
        return '\nPrivate Ad ------------------\n{text}\nActual until: {expiration_date}, {delta} days left\n'.format(
            text=self.text, expiration_date=self.expiration_date, delta=delta)
    
    
class JokeOfTheDay:
    def __init__(self, text: str) -> None:
        self.text = text

    def generate_mark(self):
        marks = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        mark = choice(marks)
        return 'Funny meter - {mark} of ten'.format(mark=mark)

    def get_joke_body(self):
        funny_meter = self.generate_mark()
        return '\nJoke of the day ------------\n{text}\n{funny_meter}\n'.format(
            text=self.text, funny_meter=funny_meter)
    

while True:
    data_type = input('------------------------------------------\nWhat type of data do you want to add? Please choose from the variants below:\n1 - News, 2 - Private Ad, 3 - Joke\nTo exit, type "exit"\n')
    if data_type.lower() == 'exit':
        break
    elif data_type not in ('1', '2', '3'):
        print('Unknown option was selected. Please try again')
        continue

    # Open the file in write mode
    file_path = 'news_feed.txt'

    with open(file_path, 'a') as file:
        file_size = path.getsize(file_path)
 
        # if file size is 0, enter first record
        if (file_size == 0): 
            file.write("News feed:")

        text = input('Please enter your text: ')

        match data_type:                
            case '1':
                city = input('Please enter the name of the city: ')
                news = News(text, city)
                file.write(news.get_news_body())
            case '2':
                while True:
                    try:
                        expiration_date = input('Please enter the expiration date (dd/mm/yyyy): ')
                        ad = PrivateAd(text, expiration_date)
                        file.write(ad.get_ad_body())
                        break
                    except ValueError:
                        print("That's not a valid date. Please try again.")
            case '3':
                joke = JokeOfTheDay(text)
                file.write(joke.get_joke_body())
