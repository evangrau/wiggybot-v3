import sys
import pathlib
import os
from dotenv import load_dotenv
from discord import Object
from loguru import logger as log

load_dotenv()

log.remove()
log.add("logs/wiggybot.log", rotation="1 week", retention="1 month", compression="zip", level="INFO")
log.add(sys.stderr, level="DEBUG", colorize=True)

COMMAND_PREFIX = "!"

MODE = "prod"

ADMIN_IDS = [294217244802678784]

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DISCORD_API_SECRET = os.getenv('DISCORD_TOKEN')

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

GUILDS_ID = Object(id=int(os.getenv('DISCORD_GUILD')))

CLIPS_CHANNEL_ID = int(os.getenv('CLIPS_CHANNEL_ID'))

GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID'))
