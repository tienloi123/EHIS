import os
from pydantic import BaseSettings

from app.constant import ProjectBuildTypes


class Settings(BaseSettings):
    PROJECT_NAME: str = "Electronic Health Information System"
    PROJECT_DESCRIPTION: str = """Powered by Tien Loi 🚀"""
    VERSION: str = "0.1-SNAPSHOT"
    ALLOW_ORIGINS: list
    DEBUG: bool = False
    PROJECT_BUILD_TYPE: str = ProjectBuildTypes.DEVELOPMENT
    # SQLAlchemy config
    SQLALCHEMY_DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_URL: str
    # OPA config
    OPA_SERVER: str
    OPA_SERVER_PORT: str
    # Authentication
    JWT_SECRET: str
    # DB config
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    # PG Admin config
    PGDATA: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    # NOSQL
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGODB_URI: str
    # PUSHER
    PUSHER_APP_ID: str
    PUSHER_KEY: str
    PUSHER_SECRET: str
    PUSHER_CLUSTER: str
    # CELERY
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


env_file = os.getenv('ENV_FILE', '.env.dev')
settings = Settings(_env_file=env_file, _env_file_encoding='utf-8')
