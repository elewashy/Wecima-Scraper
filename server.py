from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

def scrape(target_url):
    full_url = f"https://wecima.watch/watch/{target_url}"

    headers = {
        'Referer': 'https://wecima.watch/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_container = soup.find('div', class_='Download--Wecima--Single')
            
            # قواميس لتخزين الروابط حسب القسم
            quality_map_watch = {}
            quality_map_season_download = {}

            # العثور على جميع أقسام التحميل وتحديد القسم المناسب
            sections = download_container.find_all('ul', class_='List--Download--Wecima--Single')
            for section in sections:
                # فحص ما إذا كانت العنوان السابق "سيرفرات التحميل" أو "تحميل الموسم كامل"
                previous_element = section.find_previous_sibling()
                
                if previous_element and previous_element.name == "titleshape" and "سيرفرات التحميل" in previous_element.text:
                    current_map = quality_map_watch
                elif previous_element and previous_element.name == "div" and "SeasonDownload" in previous_element.get("class", []):
                    current_map = quality_map_season_download
                else:
                    continue

                # استخراج الروابط داخل القسم الحالي
                links = section.find_all('a', class_='hoverable activable')
                for link in links:
                    video_link = link['href']
                    video_link = video_link.replace("https://tgb4.top15top.shop", "https://uupbom.com/")
                    
                    resolution = link.find('resolution').text.strip()

                    # تخزين الروابط بناءً على الجودة
                    if "1080" in resolution:
                        current_map[1080] = video_link
                    elif "720" in resolution:
                        current_map[720] = video_link
                    elif "480" in resolution:
                        current_map[480] = video_link
                    elif "360" in resolution:
                        current_map[360] = video_link
                    elif "240" in resolution:
                        current_map[240] = video_link
                    elif "غير محدد" in resolution:
                        current_map[000] = video_link

            # تحويل الروابط إلى الشكل المطلوب
            links_download = {quality: f"/download/{target_url}" for quality in quality_map_watch.keys()}
            links_season_download = {quality: f"/download/{target_url}" for quality in quality_map_season_download.keys()}

            episode_links = []
            episodes_container = soup.find('div', class_='Seasons--Episodes')
            if episodes_container:
                episodes = episodes_container.find_all('a', class_='hoverable activable')
                for episode in episodes:
                    episode_url = episode['href'].replace("https://wecima.watch", "")  # إزالة الدومين
                    
                    # تحقق من وجود العنصر
                    title_element = episode.find('episodetitle')
                    if title_element:
                        episode_title = title_element.text.strip()
                        episode_links.append({'url': episode_url, 'title': episode_title})
                    else:
                        print("لم يتم العثور على عنوان الحلقة.")

            # تمرير الروابط للقالب
            return render_template(
                'template.html',
                links_watch=quality_map_watch,
                links_download=links_download,
                links_season_download=links_season_download,
                episode_links=episode_links
            )
        
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500
##########################################################Download
def download_view(target_url):
    full_url = f"https://wecima.watch/watch/{target_url}"

    headers = {
        'Referer': 'https://wecima.watch/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_section = soup.find('div', class_='Download--Wecima--Single')

            if download_section:
                # قاموسين للسيرفرات العادية
                quality_map_watch = {}
                quality_map_download = {}
                
                # قاموسين لتحميل الموسم كامل
                season_links_watch = {}
                season_links_download = {}

                # الحصول على روابط التحميل داخل الأقسام
                sections = download_section.find_all('ul', class_='List--Download--Wecima--Single')
                
                # تحديد القسم بناءً على تواجد "SeasonDownload"
                for i, section in enumerate(sections):
                    is_season_download = section.find_previous_sibling('div', class_='SeasonDownload') is not None
                    links = section.find_all('a', class_='hoverable activable')

                    for link in links:
                        video_link = link['href']
                        video_link = video_link.replace("https://tgb4.top15top.shop", "https://uupbom.com/")
                        
                        resolution = link.find('resolution').text.strip()

                        # إضافة الروابط للقاموس المناسب بناءً على الجودة
                        if "1080" in resolution:
                            if is_season_download:
                                season_links_watch[1080] = video_link
                            else:
                                quality_map_watch[1080] = video_link
                        elif "720" in resolution:
                            if is_season_download:
                                season_links_watch[720] = video_link
                            else:
                                quality_map_watch[720] = video_link
                        elif "480" in resolution:
                            if is_season_download:
                                season_links_watch[480] = video_link
                            else:
                                quality_map_watch[480] = video_link
                        elif "360" in resolution:
                            if is_season_download:
                                season_links_watch[360] = video_link
                            else:
                                quality_map_watch[360] = video_link
                        elif "240" in resolution:
                            if is_season_download:
                                season_links_watch[240] = video_link
                            else:
                                quality_map_watch[240] = video_link
                        elif "غير محدد" in resolution:
                            if is_season_download:
                                season_links_watch[000] = video_link
                            else:
                                quality_map_watch[000] = video_link

                # استخراج روابط الحلقات وتعديل الروابط
                episode_links = []
                episodes_container = soup.find('div', class_='Seasons--Episodes')
                if episodes_container:
                    episodes = episodes_container.find_all('a', class_='hoverable activable')
                    for episode in episodes:
                        episode_url = episode['href'].replace("https://wecima.watch", "").replace("/watch", "/download")  # تعديل الرابط ليبدأ بـ /download
                        
                        # تحقق من وجود العنصر
                        title_element = episode.find('episodetitle')
                        if title_element:
                            episode_title = title_element.text.strip()
                            episode_links.append({'url': episode_url, 'title': episode_title})
                        else:
                            print("لم يتم العثور على عنوان الحلقة.")

                # تمرير الروابط للقالب بعد تقسيمها
                return render_template(
                    'download_view.html',
                    links_watch=quality_map_watch,
                    links_download=quality_map_download,
                    season_links_watch=season_links_watch,
                    season_links_download=season_links_download,
                    episode_links=episode_links  # تمرير روابط الحلقات المعدلة للقالب
                )
            else:
                return "Download section not found.", 404
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500
