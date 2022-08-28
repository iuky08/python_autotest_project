#-*- coding: utf-8 -*-
import os
from dotenv import load_dotenc
from urllib3 import disable_warnings

@pytest.fixture(autouse=True, scope="session")
def load_env():
    """Загружает всё из файла .env и подставляет в environment variables.
       Запускается автоматически один раз для всех тестов.
       """
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, verbose=True)

config = dict()
config['URL'] = os.getenv('URL', False)
config['AUTH_TOKEN'] = os.getenv('AUTH_TOKEN', False)
config['USERNAME'] = os.getenv('USERNAME', False)
config['PASSWORD'] = os.getenv('PASSWORD', False)

disable_warnings()
