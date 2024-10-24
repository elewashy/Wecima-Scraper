from flask import Flask, render_template

app = Flask(__name__)

headers = {
    'Referer': 'https://bs.cimanow.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

video_url = "https://deva-cpmav9sk6x25.cimanowtv.com/uploads/2022/11/10/_Cima-Now.CoM_%20Al.Nadaha.Siwa.2022.HD/%5BCima-Now.CoM%5D%20Al.Nadaha.Siwa.2022.HD-480p.mp4"


if __name__ == '__main__':
    app.run(debug=True)
