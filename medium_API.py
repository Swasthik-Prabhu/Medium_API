from fastapi import FastAPI, Path, HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time
import random
import logging
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import FileResponse
import os
import datetime

app = FastAPI()

# --- Download Directory Setup ---
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class Article(BaseModel):
    title: str
    description: str
    image: str
    link: str

class ScrapeResponse(BaseModel):
    results: List[Article]
    filename: Optional[str] = Field(description="The filename for downloading results")
    download_url: Optional[str] = Field(description="The URL to download the scraped data")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    return webdriver.Chrome(options=options)

def scrap_medium(query: str, max_articles: int) -> List[dict]:
    driver = init_driver()
    results = []
    try:
        logging.info(f"Searching Medium for query: {query}")
        driver.get(f"https://medium.com/search?q={query}")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        articles = driver.find_elements(By.TAG_NAME, "article")
        logging.info(f"Found {len(articles)} articles for query: {query}")
        for article in articles[:max_articles]:
            html_content = article.get_attribute("outerHTML")
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.find("h2")
                description = soup.find("h3")
                link_tag = soup.find("div", attrs={"role": "link"})
                img_tags = soup.find_all("img")
                article_data = {
                    "title": title.get_text(strip=True) if title else "",
                    "description": description.get_text(strip=True) if description else "",
                    "image": img_tags[1]['src'] if len(img_tags) > 1 and img_tags[1].has_attr('src') else "", # type: ignore
                    "link": link_tag['data-href'] if link_tag and link_tag.has_attr('data-href') else "" # type: ignore
                }
                results.append(article_data)
    except Exception as e:
        driver.save_screenshot("screenshot.png")
        logging.error(f"Error with query '{query}': {e}")
    finally:
        driver.quit()
    return results

def generate_filename(query: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c if c.isalnum() else "_" for c in query.strip())[:20] 
    return f"{safe_query}_{timestamp}.json"

# ——— Download Endpoint ———
@app.get("/medium/download/{filename}", summary="Download a scraped Medium data file by filename")
def download_data(filename: str = Path(..., description="Filename of the scraped Medium data to download", example="DevOps_20231001_123456.json")):
    """Download a specific scraped Medium articles file as a JSON file."""
    if "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename requested.")
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Data file not found for download.")
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/json"
    )

# ——— Scraping Endpoint ———
@app.get('/medium/{query}/{max_articles}', response_model=ScrapeResponse, summary="Scrape Medium articles and get results + download filename")
def scrap_function(
    query: str = Path(..., description="Search query for Medium articles", example="DevOps"),
    max_articles: int = Path(..., description="Number of articles to fetch for the query", example=5, ge=1, lt=30)
):
    """Scrape Medium articles for a search query."""
    scraped_data = scrap_medium(query, max_articles)
    filename = generate_filename(query)
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)
            logging.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")
    base_url = "http://localhost:8000"
    download_url = f"{base_url}/medium/download/{filename}"
    results = [Article(**article) for article in scraped_data]
    return ScrapeResponse(results=results, filename=filename, download_url=download_url)
