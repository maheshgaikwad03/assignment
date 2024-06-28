import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kjcnjkck/jcnlkjncackkckac'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:root@localhost/logindb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
