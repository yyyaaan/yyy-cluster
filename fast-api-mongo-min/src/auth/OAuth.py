# Yan Pan, 2023
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

from settings.settings import Settings

settings = Settings()

oauth = OAuth(Config(environ={
    'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID, 
    'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET}
))
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
