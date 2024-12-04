# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cabanas_user:your_secure_password@localhost/cabanas_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'