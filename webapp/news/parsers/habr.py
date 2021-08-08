from bs4 import BeautifulSoup
from datetime import datetime
from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news


def get_habr_news_snipets():
    html = get_html('https://habr.com/ru/hub/python/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')
        for i in all_news:
            title = i.find('a', class_='tm-article-snippet__title-link').text
            url_title = f"https://habr.com{i.find('a', class_='tm-article-snippet__title-link')['href']}"
            published_title = i.find('span', class_='tm-article-snippet__datetime-published').find('time')['title']
            published = datetime.strptime(published_title, "%Y-%m-%d, %H:%M")
            save_news(title, url_title, published)

def get_habr_news_text():
    news_none_text = News.query.filter(News.text.is_(None))
    for news in news_none_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='article-formatted-body').decode_contents()
            news.text = news_text
            db.session.add(news)
            db.session.commit()
