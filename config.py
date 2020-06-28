import os

class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or "jndsfkjdwi7ifgd7adfdkqebdjkquiegd332i7ge128hel1bned1uiged"
    