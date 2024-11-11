from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()
@dataclass
class Config:
    token: str = os.getenv('TELEGRAM_BOT_TOKEN')
    admin_id: int = os.getenv('ADMIN_ID')
    pay_token: str = os.getenv('PAY_TOKEN')

    name_db: str = os.getenv('POSTGRES_DB')
    user_db: str = os.getenv('POSTGRES_USER')
    password_db: str = os.getenv('POSTGRES_PASSWORD')
    host_db: str = os.getenv('POSTGRES_HOST')

