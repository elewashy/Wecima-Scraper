import requests
from bs4 import BeautifulSoup
import re

def get_series(page_number=1):
    url = f"https://wecima.stream/page/{page_number}/"
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
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
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
