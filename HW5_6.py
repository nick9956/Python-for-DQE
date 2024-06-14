from datetime import datetime
from random import choice
from os import path, remove
from HW_4_3 import normalize_text


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
    

class FileReader:

    def __init__(self, file_path: str = 'data.txt'):
        self.file_path = file_path

    def read_file(self):
        records = []
        with open(self.file_path, 'r', encoding='utf8') as file:
            records = file.readlines()        
        return records
    
    def delete_read_file(self):
        remove(self.file_path)


class FilePublisher:

    def __init__(self, file_path: str = 'news_feed.txt'):
        self.file_path = file_path

    def check_file_size(self):
        return path.getsize(self.file_path)
 
    def publish_record(self, data_type):
        with open(self.file_path, 'a') as file:
            file_size = self.check_file_size()
    
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

    def publish_records(self, records):
        with open(self.file_path, 'a') as file:
            file_size = self.check_file_size()
    
            # if file size is 0, enter first record
            if (file_size == 0):
                file.write("News feed:\n")

            for record in records:
                normalize_record = normalize_text(record)
                file.write(normalize_record)


while True:
    method = input('------------------------------------------\nHow do you want to add a data? Please choose from the variants below:\n1 - Manually, 2 - From File\nTo exit, type "exit"\n')

    if method.lower() == 'exit':
        break
    elif method == '1':
        data_type = input('What type of data do you want to add? Please choose from the variants below:\n1 - News, 2 - Private Ad, 3 - Joke\n')
        publisher = FilePublisher()
        publisher.publish_record(data_type)
        if data_type not in ('1', '2', '3'):
            print('Unknown option was selected. Please try again')
            continue
    elif method == '2':
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')
        if location == '1':
            reader = FileReader()
            records = reader.read_file()
            reader.delete_read_file()
            publisher = FilePublisher()
            publisher.publish_records(records)
        elif location == '2':
            new_location = input('Please enter new file location\n')
            reader = FileReader(new_location)
            records = reader.read_file()
            reader.delete_read_file()
            publisher = FilePublisher()
            publisher.publish_records(records)
        else:
            print('Unknown option was selected. Please try again\n')
            continue
    else:
        print('Unknown option was selected. Please try again\n')
        continue
