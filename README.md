# 🎬 Wecima Scraper

A Flask-based web application for scraping and displaying movies and TV series from Wecima with a modern Arabic user interface.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone)

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## ✨ Features

- 🎭 **Comprehensive Content Library**: Browse movies and TV series by category
- 🔍 **Smart Search**: Search functionality for finding specific content
- 🌍 **Multi-language Content**: Support for Arabic, English, Turkish, Indian, and Asian content
- 📺 **Series Management**: View series with episodes organized by seasons
- 🎬 **Movie Categories**: 
  - Arabic Movies
  - English Movies
  - Turkish Movies
  - Indian Movies
  - Documentary Movies
  - Movie Collections
- 📱 **Responsive Design**: Modern UI with Arabic language support
- 🎪 **Special Collections**: Ramadan series from different years (2020-2025)
- ⚡ **Fast Performance**: Optimized scraping and caching mechanisms
- 🔗 **Direct Links**: Watch and download links for content

## 🛠 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/elewashy/wecima-scraper.git
   cd wecima-scraper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage

### Local Development

```bash
python app.py
```

The application will start in debug mode and be available at `http://localhost:5000`.

### Production Deployment

```bash
python app.py
```

## 🛣 API Endpoints

### Main Pages
- `GET /` - Home page with latest content
- `GET /page/<int:page_number>/` - Paginated home page

### Search
- `GET /search/<query>` - Search for movies/series

### Movies
- `GET /movies/page/<int:page_number>/` - All movies
- `GET /arabic-movies/page/<int:page_number>/` - Arabic movies
- `GET /english-movies/page/<int:page_number>/` - English movies
- `GET /turkish-movies/page/<int:page_number>/` - Turkish movies
- `GET /india-movies/page/<int:page_number>/` - Indian movies
- `GET /documentary-movies/page/<int:page_number>/` - Documentary movies
- `GET /full-pack/page/<int:page_number>/` - Movie collections

### TV Series
- `GET /series-1/page/<int:page_number>/` - All series
- `GET /english-series/page/<int:page_number>/` - English series
- `GET /arabic-series/page/<int:page_number>/` - Arabic series
- `GET /turkish-series/page/<int:page_number>/` - Turkish series
- `GET /indian-series/page/<int:page_number>/` - Indian series
- `GET /asian-series/page/<int:page_number>/` - Asian series
- `GET /documentary-series/page/<int:page_number>/` - Documentary series

### Ramadan Specials
- `GET /ramadan-2025-series/page/<int:page_number>/` - Ramadan 2025 series
- `GET /ramadan-2024-series/page/<int:page_number>/` - Ramadan 2024 series
- `GET /ramadan-2023-series/page/<int:page_number>/` - Ramadan 2023 series
- `GET /ramadan-2022-series/page/<int:page_number>/` - Ramadan 2022 series
- `GET /ramadan-2021-series/page/<int:page_number>/` - Ramadan 2021 series
- `GET /ramadan-2020-series/page/<int:page_number>/` - Ramadan 2020 series

### Content Access
- `GET /series/<path:series_name>/` - View series episodes
- `GET /watch/<path:target_url>` - Watch content
- `GET /download/<path:target_url>` - Download content

## 📁 Project Structure

```
wecima-scraper/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment configuration
├── movies.py           # Movie scraping functions
├── series.py           # TV series scraping functions
├── latest.py           # Latest content functions
├── search.py           # Search functionality
├── server.py           # Core scraping and server functions
├── static/             # Static assets
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── fonts/         # Font files
│   └── images/        # Image assets
└── templates/          # HTML templates
    ├── template.html  # Base template
    ├── series.html    # Series listing template
    ├── All_series.html # Series detail template
    ├── search.html    # Search results template
    └── download_view.html # Download page template
```





## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is for educational purposes only. The scraping functionality is designed to interact with publicly available content. Users are responsible for ensuring their use complies with applicable laws and the terms of service of the target websites.

**Important Notes:**
- Respect robots.txt and rate limiting
- Use responsibly and ethically
- Consider the legal implications in your jurisdiction
- The developers are not responsible for any misuse of this software

## 🛡️ Security

If you discover any security vulnerabilities, please send an email to the maintainers instead of using the issue tracker.


**Built with ❤️ By Elewashy**