#-*- coding: utf-8 -*-
import os
from dotenv import load_dotenc
from urllib3 import disable_warnings

dotenv_path = os.path.join(os.path.dirname(__file__), .env)
if os.path.exists(dotenv_path, verbose = True)

config = dict()
config['URL'] = os.getenv('URL', False)
config['AUTH_TOKEN'] = os.getenv('AUTH_TOKEN', False)
config['USERNAME'] = os.getenv('USERNAME', False)
config['PASSWORD'] = os.getenv('PASSWORD', False)

disable_warnings()
