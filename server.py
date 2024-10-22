from flask import render_template
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

                return render_template('download_view.html', links=quality_map)
            else:
                return "Download section not found.", 404
        else:
            return "Failed to retrieve the target page.", 500
    except Exception as e:
        return str(e), 500
