import requests
from bs4 import BeautifulSoup
import re
###########################################################arabic
def fetch_movies(page_number=1):
    url = f"https://wecima.stream/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/movies/page/{page_number_text}/"
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

def get_arabic_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/افلام-عربي-arabic-movies/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/arabic-movies/page/{page_number_text}/"
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

##############################################################English
def get_english_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/10-movies-english-افلام-اجنبي/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/english-movies/page/{page_number_text}/"
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

############################################################################3india
def get_indian_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/افلام-هندي-indian-movies/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/indian-movies/page/{page_number_text}/"
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

##########################################################Turkish

def get_turkish_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/1-افلام-تركى-turkish-films/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/turkish-movies/page/{page_number_text}/"
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


###########################################################################documentary

def get_documentary_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/1-افلام-وثائقية-documentary-films/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/documentary-movies/page/{page_number_text}/"
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

###############################################################fullpack movies

def get_full_pack_movies(page_number=1):
    url = f"https://wecima.stream/category/أفلام/10-movies-english-افلام-اجنبي/1-سلاسل-الافلام-الكاملة-full-pack/?page_no={page_number}"
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
            
            if link.startswith("https://wecima.stream"):
                link = link.replace("https://wecima.stream", "")
            
            episode = None  # للأفلام لا حاجة للحلقات
            
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
                page_url = f"/full-pack/page/{page_number_text}/"
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
