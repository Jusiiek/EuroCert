import os

HERE = os.getcwd()
FIXTURES_PATH = os.path.join(HERE, 'fixtures')

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
ORIGINS = ["localhost:3000"]
