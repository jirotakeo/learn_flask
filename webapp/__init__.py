from flask import Flask, render_template
from webapp.weather import weather_by_city
from webapp.python_news import get_python_news


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    @app.route('/')
    def index():
        page_title = 'Прогноз погоды'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = get_python_news()
        return render_template('index.html', page_title=page_title, weather_text=weather, news_list=news_list)
    return app

# if __name__ == "__main__":
#     app.run(debug=True)
