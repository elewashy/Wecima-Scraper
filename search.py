import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote

def search_series(query):
    # ترميز الكلمة البحثية
    query_encoded = quote(query)
    url = f"https://wecima.movie/search/{query_encoded}/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # أثار استثناء إذا كان هناك خطأ في الطلب
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []  # ارجع قائمة فارغة في حال حدوث خطأ
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    series = []
    
    series_container = soup.find("div", class_="Grid--WecimaPosts")
    
    if series_container:
        series_elements = series_container.find_all("div", class_="Thumb--GridItem")

        for element in series_elements:
            title_element = element.find("strong", class_="hasyear")
            title = title_element.text.strip() if title_element else "عنوان غير متوفر"
            
            link_element = element.find("a")
            link = link_element["href"] if link_element else "#"
            
            # تأكد من أن الرابط يبدأ بـ https://wecima.movie
            if not link.startswith("https://wecima.movie"):
                link = "https://wecima.movie" + link
            
            episode_element = element.find("div", class_="Episode--number")
            episode = episode_element.text.strip().replace("حلقة", "").strip() if episode_element else None
            
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
    else:
        print("No series container found in the response.")
    
    return series
