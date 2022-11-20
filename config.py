import os


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'privet will day its okey'
