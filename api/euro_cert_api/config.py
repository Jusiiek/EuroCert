import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(HERE, 'fixtures')

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'euro_cert')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ORIGINS = ["localhost:3000"]
