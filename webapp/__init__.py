from flask import Flask, render_template
from webapp.weather import weather_by_city

from webapp.model import db, News


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = 'Прогноз погоды'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=page_title, weather_text=weather, news_list=news_list)
    return app

# if __name__ == "__main__":
#     app.run(debug=True)
