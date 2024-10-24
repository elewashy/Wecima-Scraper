from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from movies import get_arabic_movies, get_english_movies, get_indian_movies, get_turkish_movies, get_documentary_movies, get_full_pack_movies, fetch_movies
from latest import get_series
from search import search_series
from server import scrape, download_view
from series import get_english_series, get_arabic_series, get_indian_series, get_asian_series, get_turkish_series, get_documentary_series, get_ramadan_series_2024, get_ramadan_series_2023, get_ramadan_series_2022, get_ramadan_series_2021, get_ramadan_series_2020, fetch_series, get_series_episodes
import re

app = Flask(__name__)
@app.route('/video')
def video():
    return render_template('video.html', video_url=video_url)

@app.route('/')
@app.route('/page/<int:page_number>/')  # إضافة مسار للصفحات
def index(page_number=1):
    series, pagination = get_series(page_number)  # تمرير رقم الصفحة إلى الدالة
    page_title = "المضاف حديثا"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/search/<query>')  # المسار الآن يعتمد على الكلمة بعد /search/
def search(query):
    series = search_series(query)  # استدعاء دالة البحث باستخدام الكلمة
    page_title = f"نتائج البحث عن : {query}"
    return render_template('search.html', series=series, page_title=page_title)

@app.route('/series/<path:series_name>/')  
def series_page(series_name):
    series_data = get_series_episodes(series_name)

    if series_data:
        page_title = series_data['title']
        episodes = series_data['episodes']
        return render_template('series.html', series=episodes, page_title=page_title)
    else:
        return "المسلسل غير موجود.", 404

@app.route('/watch/<path:target_url>', methods=['GET'])
def watch_route(target_url):
    return scrape(target_url)

@app.route('/download/<path:target_url>')
def download_route(target_url):
    return download_view(target_url)

@app.route('/movies/page/<int:page_number>/', methods=['GET'])
def render_movies(page_number=1):
    series, pagination = fetch_movies(page_number)
    page_title = "الأفلام"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/arabic-movies/page/<int:page_number>/', methods=['GET'])
def arabic_movies(page_number=1):
    series, pagination = get_arabic_movies(page_number)
    page_title = "الأفلام العربية "
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/english-movies/page/<int:page_number>/', methods=['GET'])
def english_movies(page_number=1):
    series, pagination = get_english_movies(page_number)
    page_title = "الأفلام الأجنبية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/india-movies/page/<int:page_number>/', methods=['GET'])
def indian_movies(page_number=1):
    series, pagination = get_indian_movies(page_number)
    page_title = "الأفلام هندية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/turkish-movies/page/<int:page_number>/', methods=['GET'])
def turkish_movies(page_number=1):
    series, pagination = get_turkish_movies(page_number)
    page_title = "الأفلام تركية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/documentary-movies/page/<int:page_number>/', methods=['GET'])
def documentary_movies(page_number=1):
    series, pagination = get_documentary_movies(page_number)
    page_title = "الأفلام وثائقية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/full-pack/page/<int:page_number>/', methods=['GET'])
def full_pack_movies(page_number=1):
    series, pagination = get_full_pack_movies(page_number)
    page_title = "سلاسل الأفلام الكاملة"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

###############################Series
@app.route('/series-1/page/<int:page_number>/', methods=['GET'])
def render_series(page_number=1):
    series, pagination = fetch_series(page_number)
    page_title = "المسلسلات"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/english-series/page/<int:page_number>/', methods=['GET'])
def english_series(page_number=1):
    series, pagination = get_english_series(page_number)
    page_title = "المسلسلات الأجنبية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/arabic-series/page/<int:page_number>/', methods=['GET'])
def arabic_series(page_number=1):
    series, pagination = get_arabic_series(page_number)
    page_title = "المسلسلات العربية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/indian-series/page/<int:page_number>/', methods=['GET'])
def indian_series(page_number=1):
    series, pagination = get_indian_series(page_number)
    page_title = "المسلسلات الهندية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/asian-series/page/<int:page_number>/', methods=['GET'])
def asian_series(page_number=1):
    series, pagination = get_asian_series(page_number)
    page_title = "المسلسلات الآسيوية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/turkish-series/page/<int:page_number>/', methods=['GET'])
def turkish_series(page_number=1):
    series, pagination = get_turkish_series(page_number)
    page_title = "المسلسلات التركية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/documentary-series/page/<int:page_number>/', methods=['GET'])
def documentary_series(page_number=1):
    series, pagination = get_documentary_series(page_number)
    page_title = "المسلسلات الوثائقية"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/ramadan-series/page/<int:page_number>/', methods=['GET'])
def ramadan_series(page_number=1):
    series, pagination = get_ramadan_series_2024(page_number)
    page_title = "مسلسلات رمضان 2024"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/ramadan-2023-series/page/<int:page_number>/', methods=['GET'])
def ramadan_2023_series(page_number=1):
    series, pagination = get_ramadan_series_2023(page_number)
    page_title = "مسلسلات رمضان 2023"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/ramadan-2022-series/page/<int:page_number>/', methods=['GET'])
def ramadan_2022_series(page_number=1):
    series, pagination = get_ramadan_series_2022(page_number)
    page_title = "مسلسلات رمضان 2022"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/ramadan-2021-series/page/<int:page_number>/', methods=['GET'])
def ramadan_2021_series(page_number=1):
    series, pagination = get_ramadan_series_2021(page_number)
    page_title = "مسلسلات رمضان 2021"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

@app.route('/ramadan-2020-series/page/<int:page_number>/', methods=['GET'])
def ramadan_2020_series(page_number=1):
    series, pagination = get_ramadan_series_2020(page_number)
    page_title = "مسلسلات رمضان 2020"
    return render_template('series.html', series=series, pagination=pagination, page_title=page_title)

if __name__ == '__main__':
    app.run(debug=True)
