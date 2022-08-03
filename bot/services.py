import time
from datetime import datetime

import aiohttp
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from config import logger


# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         title, filename = func(*args, **kwargs)
#         end = time.time()
#         result_time = end - start
#         return title, filename, result_time
#     return wrapper


# @timer
async def get_screenshot(user_id: str, url: str) -> tuple[str, str, float]:
    """Gets screenshot of the page, saves it to file, gets page title
    and calculates working time"""
    start_time = time.time()
    current_date = datetime.now().strftime("%d_%m_%Y")
    url_domain = url.split("/")[2][4:]
    filename = f"./media/{current_date}_{user_id}_{url_domain}.png"
    with webdriver.Remote(
        "http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME
    ) as driver:
        driver.set_page_load_timeout(15)
        try:
            driver.get(url)
            # await asyncio.sleep(2)
            title = driver.title
            driver.get_screenshot_as_file(filename=filename)
        except Exception as e:
            logger.error(f"{e} in request for {url}")
        # finally:
        # driver.close()
        # driver.quit()
    result_time = time.time() - start_time
    return title, filename, result_time


async def check_url(url: str) -> bool:
    """Checks if url is valid"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status_code = response.status
            if 199 < status_code < 400:
                logger.info(f"Url: {url}, status code: {status_code}")
                return True
    logger.error(f"Сайт недоступен. Url: {url}, status code: {status_code}")
    return False
