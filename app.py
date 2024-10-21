from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# دالة لجلب البيانات من الموقع
def get_series(page_number=1):
    url = f"https://wecima.movie/page/{page_number}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    series = []
    
    # البحث عن القسم الذي يحتوي على المسلسلات
    series_container = soup.find("div", class_="Grid--WecimaPosts")
    
    if series_container:
        series_elements = series_container.find_all("div", class_="Thumb--GridItem")

        for element in series_elements:
            title_element = element.find("strong", class_="hasyear")
            title = title_element.text.strip() if title_element else "عنوان غير متوفر"
            
            link_element = element.find("a")
            link = link_element["href"] if link_element else "#"
            
            # تعديل الرابط ليكون /watch وباقي الرابط
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
            # البحث عن رقم الحلقة
            episode_element = element.find("div", class_="Episode--number")
            episode = episode_element.text.strip().replace("حلقة", "").strip() if episode_element else None
            
            # استخراج رابط الصورة من خاصية data-lazy-style
            bg_image_element = element.find("span", class_="BG--GridItem")
            image_url = "رابط صورة غير متوفر"
            
            if bg_image_element:
                lazy_style_value = bg_image_element.get('data-lazy-style', '')
                image_url_match = re.search(r'url\((.*?)\)', lazy_style_value)
                if image_url_match:
                    image_url = image_url_match.group(1).strip('\"')

            series.append({
                "title": title,
                "link": link,  # الآن link هو الرابط المعدل
                "image_url": image_url,
                "episode": episode
            })
    
    # جلب أرقام الصفحات
    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = link["href"]
                is_active = str(page_number) == page_number_text
                pagination.append({
                    "number": page_number_text,
                    "url": page_url,
                    "active": is_active
                })
            elif current_page:
                pagination.append({
                    "number": current_page.text.strip(),
                    "url": "#",
                    "active": True
                })
            else:
                pagination.append({
                    "number": page.find("span").text.strip(),
                    "url": "#",
                    "active": False
                })

    return series, pagination

@app.route('/watch/<path:target_url>', methods=['GET'])
def scrape(target_url):
    full_url = f"https://wecima.movie/watch/{target_url}"

    headers = {
        'Referer': 'https://wecima.movie/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_section = soup.find('div', class_='Download--Wecima--Single')

            if download_section:
                links = download_section.find_all('a', class_='hoverable activable')

                quality_map = {}
                for link in links:
                    video_link = link['href']
                    video_link = video_link.replace("https://tgb4.top15top.shop", "https://uupbom.com/")
                    
                    resolution = link.find('resolution').text.strip()
                    if "1080" in resolution:
                        quality_map[1080] = video_link
                    elif "720" in resolution:
                        quality_map[720] = video_link
                    elif "480" in resolution:
                        quality_map[480] = video_link
                    elif "360" in resolution:
                        quality_map[360] = video_link
                    elif "240" in resolution:
                        quality_map[240] = video_link

                return render_template('template.html', links=quality_map)
            else:
                return "Download section not found.", 404
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500
@app.route('/download/<int:quality>/<path:video_url>', methods=['GET'])
def download_page(quality, video_url):
    return render_template('download_page.html', video_url=video_url, quality=quality)

@app.route('/')
@app.route('/page/<int:page_number>/')  # إضافة مسار للصفحات
def index(page_number=1):
    series, pagination = get_series(page_number)  # تمرير رقم الصفحة إلى الدالة
    return render_template('series.html', series=series, pagination=pagination)

if __name__ == '__main__':
    app.run(debug=True)
