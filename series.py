import requests
from bs4 import BeautifulSoup
import re

def fetch_series(page_number=1):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/?page_no={page_number}"
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
            
            # البحث عن رقم الحلقة إن وجدت
            episode_element = element.find("div", class_="Episode--number")
            episode = episode_element.text.strip().replace("حلقة", "").strip() if episode_element else None
            
            # استخراج رابط الصورة
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
                page_url = f"/series-1/page/{page_number_text}/"
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
import json
from urllib.parse import urlparse

def get_series_episodes(series_name):
    url = f"https://wecima.movie/series/{series_name}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # استرجاع عنوان المسلسل
        title_div = soup.find('div', class_='Title--Content--Single-begin')
        title = title_div.h1.text if title_div else "عنوان غير متوفر"

        episodes = []

        # البحث عن البيانات في علامة <script> التي تحتوي على JSON
        script_tag = soup.find('script', type='application/ld+json')
        image_url = "رابط الصورة غير متوفر"
        
        if script_tag:
            data = json.loads(script_tag.string)
            for item in data["@graph"]:
                if "@type" in item and item["@type"] == "CollectionPage":
                    if "thumbnailUrl" in item:
                        image_url = item["thumbnailUrl"]
                        break

        # استرجاع الحلقات
        episode_elements = soup.find_all('a', class_='hoverable activable')
        for episode in episode_elements:
            episode_link = episode['href']

            # إزالة الدومين
            parsed_url = urlparse(episode_link)
            relative_link = f"{parsed_url.path}"  # الاحتفاظ فقط بالمسار

            # محاولة العثور على العنصر، وإذا لم يكن موجودًا، تجاهله
            episode_area = episode.find('episodearea')
            if episode_area:
                episode_title = episode_area.find('episodetitle').text if episode_area.find('episodetitle') else "عنوان غير متوفر"

                # إضافة بيانات الجودة
                quality = episode_area.find('quality')  # استبدل 'quality' بالعلامة الصحيحة إذا كانت مختلفة

                episodes.append({
                    'link': relative_link,  # استخدام الرابط النسبي
                    'title': episode_title,
                    'image_url': image_url,  # استخدام رابط الصورة من البيانات المستخرجة
                    'quality': quality.text if quality else None,  # تحقق من وجود الجودة
                })

        # حساب العدد الإجمالي للحلقات
        total_episodes = len(episodes)

        # إضافة رقم الحلقة بطريقة معكوسة
        for index, episode in enumerate(episodes):
            episode['episode'] = total_episodes - index  # عكس الرقم

        return {'title': title, 'image_url': image_url, 'episodes': episodes}
    
    return None

def get_english_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/6-series-english-مسلسلات-اجنبي/?page_no={page_number}"
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
            
            # البحث عن رقم الحلقة إن وجدت
            episode_element = element.find("div", class_="Episode--number")
            episode = episode_element.text.strip().replace("حلقة", "").strip() if episode_element else None
            
            # استخراج رابط الصورة
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
                page_url = f"/english-series/page/{page_number_text}/"
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

##################################arabic


def get_arabic_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/13-مسلسلات-عربيه-arabic-series/?page_no={page_number}"
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
            
            # استخراج رابط الصورة
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
                page_url = f"/arabic-series/page/{page_number_text}/"
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

###################################india

def get_indian_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/10-series-indian-مسلسلات-هندية/?page_no={page_number}"
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
            
            # استخراج رابط الصورة
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
                page_url = f"/indian-series/page/{page_number_text}/"
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

#############################Asia

def get_asian_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/1-مسلسلات-اسيوية/?page_no={page_number}"
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
            
            # استخراج رابط الصورة
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
                page_url = f"/asian-series/page/{page_number_text}/"
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

##############################Turkish

def get_turkish_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/10-مسلسلات-تركية-turkish-series/?page_no={page_number}"
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
            
            # استخراج رابط الصورة
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
                page_url = f"/turkish-series/page/{page_number_text}/"
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

############################################documentary

def get_documentary_series(page_number=1):
    url = f"https://wecima.movie/category/مسلسلات/1-مسلسلات-وثائقية-documentary-series/?page_no={page_number}"
    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/documentary-series/page/{page_number_text}/"
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

#################################Ramadan

def get_ramadan_series_2024(page_number):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/1-%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2024/page/{page_number}/"

    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/ramadan-series/page/{page_number_text}/"
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
def get_ramadan_series_2023(page_number):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/1-%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2023-series-ramadan-2023/page/{page_number}/"
    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/ramadan-2023-series/page/{page_number_text}/"
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
def get_ramadan_series_2022(page_number):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/1-%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2022/page/{page_number}/"
    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/ramadan-2022-series/page/{page_number_text}/"
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

def get_ramadan_series_2021(page_number):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/8-%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-ramadan-2021/page/{page_number}/"
    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/ramadan-2021-series/page/{page_number_text}/"
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

def get_ramadan_series_2020(page_number):
    url = f"https://wecima.movie/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/6-%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-ramadan-2020/page/{page_number}/"
    response = requests.get(url)
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
            
            if link.startswith("https://wecima.movie"):
                link = link.replace("https://wecima.movie", "")
            
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

    pagination = []
    pagination_container = soup.find("div", class_="pagination")
    
    if pagination_container:
        page_links = pagination_container.find_all("li")
        for page in page_links:
            link = page.find("a", class_="page-numbers")
            current_page = page.find("span", class_="current")
            
            if link:
                page_number_text = link.text.strip()
                page_url = f"/ramadan-2020-series-series/page/{page_number_text}/"
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
