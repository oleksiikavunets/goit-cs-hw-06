import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

DB_HOST = os.getenv('MONGO_DB_HOST')
DB_NAME = os.getenv('MONGO_INITDB_DATABASE')
DB_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
DB_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
DB_PORT = int(os.getenv('MONGO_DB_PORT'))
DB_URI = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"

HTTP_HOST = os.getenv('HTTP_HOST')
HTTP_PORT = int(os.getenv('HTTP_PORT'))

SOCKET_HOST = os.getenv('SOCKET_HOST')
SOCKET_PORT = int(os.getenv('SOCKET_PORT'))

print()