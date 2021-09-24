import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'boj_ranking.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "mysecretkeyisez"

GITHUB_CLIENT='fb0b9cd9b0766772bdfc'
GITHUB_SECRET="6dd52f5f1208786fb3b25297624b9674af01f7ff"
ADMIN=37260182

KEY_STAMP = 1011538800