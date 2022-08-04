import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

import aiohttp
from aiohttp import ClientConnectorError
from pyppeteer import launch
from tldextract import tldextract

from config import logger


async def get_screenshot(user_id: str, url: str) -> tuple[str, str, str, float]:
    """Gets screenshot of the page, saves it to file, gets page title
    and calculates working time"""
    start_time = time.time()
    current_date = datetime.now()
    current_time = datetime.now().strftime("%H-%M-%S")
    url_domain = tldextract.extract(url).registered_domain
    # create directory if it doesn't exist
    Path(f"./media/{current_date.date()}").mkdir(parents=True, exist_ok=True)
    filename = (
        f"./media/{current_date.date()}/{current_time}_{user_id}_{url_domain}.png"
    )
    browser = await launch(
        executablePath="/usr/bin/google-chrome-stable",
        headless=True,
        args=["--no-sandbox"],
    )
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})
    title = await page.title()
    await page.screenshot({"path": filename, "fullPage": True})
    result_time = time.time() - start_time
    return url_domain, title, filename, result_time


async def check_url(url: str) -> bool:
    """Checks if url is valid"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                status_code = response.status
                if 199 < status_code < 400:
                    logger.info(f"Url: {url}, status code: {status_code}")
                    return True
        except ClientConnectorError:
            logger.error(f"Сайт недоступен. Url: {url}")
    return False
