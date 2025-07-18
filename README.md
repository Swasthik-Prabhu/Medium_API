
# Medium Article Scraper API

A FastAPI-based web service to **scrape articles from Medium.com** by search query and provide results as JSON—complete with per-query downloadable result files.

## 🚀 Features

- **Scrape up to N Medium articles** via keyword search
- **Download results as uniquely named JSON files**
- **Well-documented OpenAPI/Swagger interface (`/docs`)**
- **Headless browser automation using Selenium**
- **Error handling, logging, and file security built in**
- Designed for extensibility and easy deployment (Docker-ready)

## 📦 Requirements

- Python 3.9+
- [Google Chrome](https://www.google.com/chrome/) (for Selenium)
- [ChromeDriver](https://chromedriver.chromium.org/)
- Pip packages:
  - fastapi
  - uvicorn
  - selenium
  - beautifulsoup4
  - pydantic

You can install dependencies with:
```bash
pip install -r requirements.txt
```

## 🖥️ Setup & Running Locally

1. **Clone this repository:**
    ```bash
    git clone https://github.com/Swasthik-Prabhu/Medium_API.git
    cd Medium_API
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure Chrome & ChromeDriver are installed and in your PATH.**

4. **Run the API:**
    ```bash
    uvicorn main:app --reload
    ```

5. Access the docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📝 API Endpoints

### 1. **Scrape Articles**
```http
GET /medium/{query}/{max_articles}
```
- **Path Params:**
  - `query` (*str*): Search keyword (e.g. DevOps)
  - `max_articles` (*int*): Number of articles to retrieve (1–29)
- **Returns:**
  - List of articles (`title`, `description`, `image`, `link`)
  - Unique JSON filename for your scrape
  - Direct download link for the result file

**Sample Response:**
```json
{
  "results": [
    {
      "title": "What is DevOps?",
      "description": "A quick introduction...",
      "image": "https://cdn-images...",
      "link": "https://medium.com/..."
    },
    ...
  ],
  "filename": "DevOps_20250718_181701.json",
  "download_url": "http://localhost:8000/medium/download/DevOps_20250718_181701.json"
}
```

### 2. **Download Scraped Data**
```http
GET /medium/download/{filename}
```
- **Path Param:**
  - `filename` (*str*): The filename returned by the scrape endpoint
- **Returns:** The previously scraped JSON file as a direct download.

## 📦 Docker Deployment

**Use the included `Dockerfile` to build and run:**

```bash
docker build -t medium-scraper .
docker run -p 8000:8000 medium-scraper
```

## 🛡️ Security & Notes

- All data files are saved in a `downloads/` directory for organization and safety.
- Only filenames that exist in `downloads/` can be downloaded; invalid or directory-traversal attempts are blocked.
- Each scrape creates a uniquely named file using the query and timestamp.
- For extended deployments, consider rate limiting and old file cleanup.

## 🌍 API Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) after running the app for an interactive API interface and detailed parameter documentation.

## 🛠️ Extending

- Add authentication for private APIs.
- Schedule automatic jobs or background scrapes with Celery or FastAPI BackgroundTasks.
- Deploy to Render, Koyeb, Railway, AWS (see their docs for Docker support).
- Enhance selector robustness for Medium UI changes.

## 🤝 License

MIT License
MIT License

Copyright (c) 2025 Swasthik Prabhu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## 📣 Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Medium](https://medium.com/)

**Questions, issues, or feature requests?  
Open an issue or PR!**

