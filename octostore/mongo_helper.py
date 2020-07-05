from pymongo import MongoClient
import os
import sys
from pathlib import Path

sys.path.append("..")
sys.path.append(str(Path(__file__).parent.resolve()))


class MongoHelpers:
    _client = None

    def __init__(self):
        db_name = os.getenv("MONGO_DB")
        host = os.getenv("MONGO_HOST")
        port = os.getenv("MONGO_PORT")
        username = os.getenv("MONGO_USERNAME")
        password = os.getenv("MONGO_PASSWORD")
        args = "ssl=true&retrywrites=false&ssl_cert_reqs=CERT_NONE"

        connection_uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?{args}"

        self._client = MongoClient(connection_uri)
        self._db = self._client[db_name]
        self._user_collection = self._db['user']
