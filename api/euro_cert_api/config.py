import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(HERE, 'fixtures')

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'euro_cert')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
TOKEN_LIFETIME = 60 * 60 * 24 # day
AUDIENCE: list[str] = ["euro_cert:auth"],
ORIGINS = ["localhost:3000"]

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 8000)
