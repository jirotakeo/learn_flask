import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.model import db, News

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url_title = news.find('a')['href']
            published = news.find('time').text
            print(published)
            try:
                published = datetime.strptime(published, '%B %d, %Y')
                print(f'gthdfz {published}')
            except(ValueError):
                published = datetime.now()
                print(f'secondtime {published}')
            save_news(title, url_title, published)


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()
