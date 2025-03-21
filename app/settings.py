import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    user_id: str
    project_id: str
    google_application_credentials: str
    language_code: str = 'ru-RU'

    log_level: str = 'INFO'
    log_format: str = '[%(asctime)s] [%(levelname)s] [%(name)s - %(filename)s] > %(lineno)d - %(message)s'

    class Config:
        env_file = 'src/.env'
        env_file_encoding = 'utf-8'


settings = Settings()
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'
] = settings.google_application_credentials
