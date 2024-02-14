import os
from dotenv import load_dotenv

class ConnectionService:

    def __init__(self):
        load_dotenv()

    def HOST(self):
        HOST = os.getenv('HOST')
        return HOST

    def PORT(self):
        PORT = os.getenv('PORT')
        return PORT

    def USER(self):
        USER = os.getenv('USER')
        return USER

    def PASS(self):
        PASS = os.getenv('PASS')
        return PASS
