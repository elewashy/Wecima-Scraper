from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

#######################################Watch
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

                # تخزين روابط المشاهدة فقط في هذا القاموس
                quality_map_watch = {}
                # تخزين روابط التحميل (بعد استبدال "watch" بـ "download") في هذا القاموس
                quality_map_download = {}
                
                # الرابط الحالي للصفحة
                current_url = request.url
                
                # استبدال "watch" بـ "download" في الرابط الحالي
                download_url = current_url.replace('/watch/', '/download/')
                
                for link in links:
                    # رابط المشاهدة
                    video_link_watch = link['href']
                    
                    # رابط التحميل: استبدال الدومين وتعديل "watch" إلى "download"
                    video_link_watch = video_link_watch.replace("https://tgb4.top15top.shop", "https://uupbom.com/")

                    # استخراج الجودة
                    resolution = link.find('resolution').text.strip()
                    
                    # تحديد الروابط بناءً على الجودة
                    if "1080" in resolution:
                        quality_map_watch[1080] = video_link_watch
                        quality_map_download[1080] = download_url
                    elif "720" in resolution:
                        quality_map_watch[720] = video_link_watch
                        quality_map_download[720] = download_url
                    elif "480" in resolution:
                        quality_map_watch[480] = video_link_watch
                        quality_map_download[480] = download_url
                    elif "360" in resolution:
                        quality_map_watch[360] = video_link_watch
                        quality_map_download[360] = download_url
                    elif "240" in resolution:
                        quality_map_watch[240] = video_link_watch
                        quality_map_download[240] = download_url

                # تمرير روابط المشاهدة والتحميل للقالب
                return render_template('template.html', 
                                       links_watch=quality_map_watch, 
                                       links_download=quality_map_download)
            else:
                return "Download section not found.", 404
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500

##########################################################Download
def download_view(target_url):
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

                # تخزين روابط المشاهدة فقط في هذا القاموس
                quality_map_watch = {}
                # تخزين روابط التحميل (بعد استبدال "watch" بـ "download") في هذا القاموس
                quality_map_download = {}
                
                # الرابط الحالي للصفحة
                current_url = request.url
                
                # استبدال "watch" بـ "download" في الرابط الحالي
                download_url = current_url.replace('/watch/', '/download/')
                
                for link in links:
                    # رابط المشاهدة
                    video_link_watch = link['href']
                    
                    # رابط التحميل: استبدال الدومين وتعديل "watch" إلى "download"
                    video_link_watch = video_link_watch.replace("https://tgb4.top15top.shop", "https://uupbom.com/")

                    # استخراج الجودة
                    resolution = link.find('resolution').text.strip()
                    
                    # تحديد الروابط بناءً على الجودة
                    if "1080" in resolution:
                        quality_map_watch[1080] = video_link_watch
                        quality_map_download[1080] = download_url
                    elif "720" in resolution:
                        quality_map_watch[720] = video_link_watch
                        quality_map_download[720] = download_url
                    elif "480" in resolution:
                        quality_map_watch[480] = video_link_watch
                        quality_map_download[480] = download_url
                    elif "360" in resolution:
                        quality_map_watch[360] = video_link_watch
                        quality_map_download[360] = download_url
                    elif "240" in resolution:
                        quality_map_watch[240] = video_link_watch
                        quality_map_download[240] = download_url

                # تمرير روابط المشاهدة والتحميل للقالب
                return render_template('download_view.html', 
                                       links_watch=quality_map_watch, 
                                       links_download=quality_map_download)
            else:
                return "Download section not found.", 404
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500
