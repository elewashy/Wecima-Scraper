import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def search_series(query):
    query_encoded = quote(query)  # تشفير الاستعلام
    base_urls = [
        f"https://wecima.movie/search/{query_encoded}/",
        f"https://wecima.movie/search/{query_encoded}/list/series/"
    ]

    series = []

    for url in base_urls:
        response = requests.get(url)
        response.encoding = 'utf-8'  # التأكد من أن الترميز صحيح
        soup = BeautifulSoup(response.content, "html.parser")

        # البحث عن الحاوية الرئيسية للمسلسلات
        series_container = soup.find("div", class_="Grid--WecimaPosts")
        
        if series_container:
            series_elements = series_container.find_all("div", class_="Thumb--GridItem")

            for element in series_elements:
                title_element = element.find("strong", class_="hasyear")
                title = title_element.get_text(strip=True) if title_element else "عنوان غير متوفر"

                link_element = element.find("a")
                link = link_element["href"] if link_element else "#"
                
                if link.startswith("https://wecima.movie"):
                    link = link.replace("https://wecima.movie", "")
                
                episode_element = element.find("div", class_="Episode--number")
                episode = episode_element.get_text(strip=True).replace("حلقة", "").strip() if episode_element else None
                
                bg_image_element = element.find("span", class_="BG--GridItem")
                image_url = "رابط صورة غير متوفر"
                
                if bg_image_element:
                    lazy_style_value = bg_image_element.get('data-lazy-style', '')
                    image_url_match = re.search(r'url\((.*?)\)', lazy_style_value)
                    if image_url_match:
                        image_url = image_url_match.group(1).strip('\"')

                series.append({
                    "title": title,
                    "link": link,
                    "image_url": image_url,
                    "episode": episode
                })

    # عرض النص بشكل صحيح
    print(f"نتائج البحث عن: {query}")  # عرض النص بدون فك التشفير
    return series
