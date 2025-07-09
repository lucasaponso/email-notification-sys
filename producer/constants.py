import os
from dotenv import load_dotenv

load_dotenv()

QUEUE_NAME: str = os.getenv('QUEUE_NAME')
RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST')