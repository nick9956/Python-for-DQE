import sqlite3


def fetch_data():
    conn = sqlite3.connect('news_feed.db')
    cursor = conn.cursor()

    for table in ['News', 'PrivateAd', 'JokeOfTheDay']:
        print(f'--- {table} ---')
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        print('\n')

    conn.close()


fetch_data()
