from pymongo import MongoClient
import os
import sys
from pathlib import Path
from environs import Env

sys.path.append("..")
sys.path.append(str(Path(__file__).parent.resolve()))


class MongoHelpers:
    _client = None
    _db = None
    _user_collection = None

    def __init__(self, connection_uri=None, db_name=None):
        env = Env()
        env.read_env()

        if db_name is None:
            db_name = os.getenv("MONGO_DB")

        if connection_uri is None:
            host = os.getenv("MONGO_HOST")
            port = os.getenv("MONGO_PORT")
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            args = "ssl=true&retrywrites=false&ssl_cert_reqs=CERT_NONE"

            connection_uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?{args}"

        self._client = MongoClient(connection_uri)
        self._db = self._client[db_name]
        self._user_collection = self._db['user']

    def get_client(self):
        return self._client
