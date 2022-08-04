import time
from datetime import datetime
from pathlib import Path

import aiohttp
from aiohttp import ClientConnectorError, InvalidURL
from pyppeteer import launch
from tldextract import tldextract

from config import logger


async def get_screenshot_and_info(
    user_id: str, url: str
) -> tuple[str, str, str, float]:
    """Gets screenshot of the page, saves it to file, gets page title and domain
    and calculates working time"""
    start_time = time.time()
    current_date = datetime.now()
    current_time = datetime.now().strftime("%H-%M-%S")
    url_domain = tldextract.extract(url).registered_domain
    # create directory if it doesn't exist
    Path(f"./media/{current_date.date()}").mkdir(parents=True, exist_ok=True)
    file_path = (
        f"./media/{current_date.date()}/{current_time}_{user_id}_{url_domain}.png"
    )
    try:
        browser = await launch(
            executablePath="/usr/bin/google-chrome-stable",
            headless=True,
            args=["--no-sandbox"],
        )
        page = await browser.newPage()
        await page.goto(url, {"waitUntil": "networkidle2"})
        title = await page.title()
        await page.screenshot({"path": file_path, "fullPage": True})
        await browser.close()
    except Exception as e:
        logger.error(e)
        return url_domain, "", file_path, time.time() - start_time
    result_time = time.time() - start_time
    return url_domain, title, file_path, result_time


async def check_url(url: str) -> bool:
    """Checks if url is valid"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                status_code = response.status
                if 199 < status_code < 400:
                    logger.info(f"Url: {url}, status code: {status_code}")
                    return True
        except (ClientConnectorError, InvalidURL):
            logger.error(f"Website unavailable. Url: {url}")
            return False
