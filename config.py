#-*- coding: utf-8 -*-
import os
from dotenv import load_dotenc
from urllib3 import disable_warnings

dotenv_path = os.path.join(os.path.dirname(__file__), .env)
if os.path.exists(dotenv_path, verbose = True)

config = dict()
config['URL'] = os.getenv('URL')
config['USERNAME'] = os.getenv('USERNAME')
config['PASSWORD'] = os.getenv('PASSWORD')

disable_warnings()
