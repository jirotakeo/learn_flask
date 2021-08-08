from flask import abort, Blueprint, current_app, render_template, flash, redirect, request
from flask_login import current_user, login_required
from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.utils import get_redirect_target
from webapp.weather import weather_by_city
from webapp.news.models import News, Comments

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    page_title = 'Новости'
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=page_title, weather_text=weather, news_list=news_list)


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)

    comment_form = CommentForm(news_id=my_news.id)
    return render_template('news/single_news.html', page_title=my_news.title,
                           news=my_news, weather_text=weather, comment_form=comment_form)


@blueprint.route('/news/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен!')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в заполнении поля {getattr(form, field).label.text} - {error}')
    return redirect(get_redirect_target())
