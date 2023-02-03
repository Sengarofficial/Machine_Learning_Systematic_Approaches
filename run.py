from config import Config
from app import app

if __name__ == "__main__":
    app(Config)  # app is a class or a function that ingest the configuration and runs this streamliit app 