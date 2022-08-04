import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN = os.getenv("TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(asctime)s - %(name)s - %(message)s"
)
