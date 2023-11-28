#from pydantic import BaseSettings
#from pydantic_settings import BaseSettings
from pathlib import Path
import environ
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

class Settings:
    sqlalchemy_database_url = env('SQLALCHEMY_DATABASE_URL') 
    secret_key = env('SECRET_KEY') 
    algorithm = env('ALGORITHM') 
    mail_username = env('MAIL_USERNAME') 
    mail_password = env('MAIL_PASSWORD')
    mail_from = env('MAIL_FROM')
    mail_port = env('MAIL_PORT')
    mail_server = env('MAIL_SERVER')
    
    redis_host = env('REDIS_HOST')
    redis_port = env('REDIS')

    cloudinary_api_key = env('CLOUDINARY_API_KEY')
    cloudinary_api_secret = env('CLOUDINARY_API_SECRET')
    cloudinary_name = env('CLOUDINARY_NAME')



settings = Settings()
