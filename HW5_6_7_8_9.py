import csv
import xml.etree.ElementTree as ET
from json import load
from datetime import datetime
from random import choice
from os import path, remove
from HW_4_3 import normalize_text
from re import sub


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
        return ['\n'] + records

    def delete_read_file(self):
        remove(self.file_path)


class JSONReader:

    def __init__(self, file_path: str = 'data.json'):
        self.file_path = file_path

    def load_file(self):
        data = []
        with open(self.file_path, 'r', encoding='utf8') as file:
            data = load(file)      
        return data

    def delete_read_file(self):
        remove(self.file_path)


class XMLReader:

    def __init__(self, file_path: str = 'data.xml'):
        self.file_path = file_path

    def read_file(self):
        root = ET.parse(self.file_path)
        data = []
        for item in root.findall('item'):
            item_data = {}
            item_data['method'] = item.find('method').text
            item_data['text'] = item.find('text').text

            # Check for other fields
            city = item.find('city')
            if city is not None:
                item_data['city'] = city.text

            current_date = item.find('current_date')
            if current_date is not None:
                item_data['current_date'] = current_date.text

            actual_until = item.find('actual_until')
            if actual_until is not None:
                item_data['actual_until'] = actual_until.text

            days_left = item.find('days_left')
            if days_left is not None:
                item_data['days_left'] = days_left.text

            funny_mark = item.find('funny_mark')
            if funny_mark is not None:
                item_data['funny_mark'] = funny_mark.text

            data.append(item_data)
        return data

    def delete_read_file(self):
        remove(self.file_path)


class FilePublisher:

    def __init__(self, file_path: str = 'news_feed.txt'):
        self.file_path = file_path

    def check_file_size(self):
        return path.getsize(self.file_path)

    def transform_to_text(self, records):
        data = ''
        for record in records:           
            method = record['method']
            hyphens = ' -------------------------\n'
            text = record['text']
            data += '\n' + method + hyphens + text + '\n'
            if method == 'News':
                data += '{city}, {date}\n'.format(city = record['city'], date = record['current_date'])
            elif method == 'Private ad':
                data += 'Actual until: {date_until}, {days_left}\n'.format(
                                    date_until = record['actual_until'], days_left = record['days_left'])
            elif method == 'Joke of the day':
                data += record['funny_mark'] + '\n'
        return data

    def publish_record(self, data_type):
        with open(self.file_path, 'a') as file:
            file_size = self.check_file_size()
    
            # if file size is 0, enter first record
            if (file_size == 0):
                file.write("News feed:\n")

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


class FileProcessor:

    def __init__(self, reader_path='data.txt', publisher_path='news_feed.txt'):
        self.reader = FileReader(reader_path)
        self.publisher = FilePublisher(publisher_path)

    def process_file(self):
        records = self.reader.read_file()
        self.reader.delete_read_file()
        self.publisher.publish_records(records)


class JSONProcessor:

    def __init__(self, reader_path='data.json', publisher_path='news_feed.txt'):
        self.reader = JSONReader(reader_path)
        self.publisher = FilePublisher(publisher_path)

    def process_file(self):
        list_of_dicts = self.reader.load_file()
        self.reader.delete_read_file()
        records = self.publisher.transform_to_text(list_of_dicts)
        self.publisher.publish_records(records)


class XMLProcessor:

    def __init__(self, reader_path='data.xml', publisher_path='news_feed.txt'):
        self.reader = XMLReader(reader_path)
        self.publisher = FilePublisher(publisher_path)

    def process_file(self):
        list_of_dicts = self.reader.read_file()
        self.reader.delete_read_file()
        records = self.publisher.transform_to_text(list_of_dicts)
        self.publisher.publish_records(records)


class SCVGenerator:

    def __init__(self, file_path: str = 'news_feed.txt'):
        self.file_path = file_path

    def get_text(self):
        with open(self.file_path) as file:
            text = file.read()
        text = text.replace('\n', ' ').replace('\r', '')
        text = sub(r'[^\w\s]|[\d]', ' ', text)  # Remove non-word characters and digits
        text = sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        return text

    def count_word(self):
        text = self.get_text().lower()
        words = text.split()
        words_counter = {}
        for word in words:
            words_counter[word] = words_counter.get(word, 0) + 1
        return words_counter

    def count_letter(self):
        letters = list(self.get_text())
        count_all_letters = len(letters)
        count_letter = []
        for letter in letters:
            if letter == ' ':
                continue
            upper = 0
            if letter.isupper():
                letter = letter.lower()
                upper = 1
            for dictionary in count_letter:
                if letter == dictionary.get('letter'):
                    dictionary['count_all'] += 1
                    dictionary['count_upper'] += upper
                    dictionary['percentage'] = (dictionary['count_all'] / count_all_letters)*100
                    break
            else:
                count_letter.append({'letter': letter, 'count_all': 1, 'count_upper': upper, 'percentage': (1/count_all_letters)*100})
        return count_letter

    def create_count_words_csv(self):
        count_words = self.count_word()
        with open('count_words.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='-')
            for key, value in count_words.items():
                writer.writerow([key, value])

    def create_count_letters_csv(self):
        count_letter = self.count_letter()
        keys = count_letter[0].keys()
        with open('count_letters.csv', 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(count_letter)


while True:
    method = input('------------------------------------------\nHow do you want to add a data? Please choose from the variants below:\n1 - Manually, 2 - From Text File, 3 - From JSON File, 4 - From XML File\nTo exit, type "exit"\n')

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
            processor = FileProcessor()
            processor.process_file()
        elif location == '2':
            new_location = input('Please enter new file location\n')
            processor = FileProcessor(reader_path=new_location)
            processor.process_file()
        else:
            print('Unknown option was selected. Please try again\n')
            continue
    elif method == '3':
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')
        if location == '1':
            processor = JSONProcessor()
            processor.process_file()
        elif location == '2':
            new_location = input('Please enter new file location\n')
            processor = JSONProcessor(reader_path=new_location)
            processor.process_file()
        else:
            print('Unknown option was selected. Please try again\n')
            continue
    elif method == '4':
        location = input('Do you want to use default path file location or enter new?\n1 - Default, 2 - New\n')
        if location == '1':
            processor = XMLProcessor()
            processor.process_file()
        elif location == '2':
            new_location = input('Please enter new file location\n')
            processor = XMLProcessor(reader_path=new_location)
            processor.process_file()
        else:
            print('Unknown option was selected. Please try again\n')
            continue
    else:
        print('Unknown option was selected. Please try again\n')
        continue

    csv_files = SCVGenerator()
    csv_files.create_count_words_csv()
    csv_files.create_count_letters_csv()
