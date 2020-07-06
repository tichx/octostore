import os
import sys
from pathlib import Path
from octostore.mongo_helper import MongoHelpers
from octostore.run import Run
from environs import Env

sys.path.append("..")
sys.path.append(str(Path(__file__).parent.resolve()))


class Client:
    _client = None
    _db = None
    _user_collection = None
    _mh = None
    _current_run = None

    def __init__(self):
        env = Env()
        env.read_env()

        connection_uri = None
        db_name = os.getenv("MONGO_DB")
        host = os.getenv("MONGO_HOST")

        if host is not None:
            port = os.getenv("MONGO_PORT")
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            args = "ssl=true&retrywrites=false&tlsAllowInvalidCertificates=true"

            connection_uri = (
                f"mongodb://{username}:{password}@{host}:{port}/{db_name}?{args}"
            )

        self._mh = MongoHelpers(connection_uri)
        self._client = self._mh.get_client()
        self._db = self._client[db_name]
        self._user_collection = self._db["user"]

    def create_run(self, experiment_id, start_time, tags):
        self._current_run = Run(experiment_id=experiment_id, start_time=start_time, tags=tags)
        return self.get_current_run()

    def get_current_run(self):
        return self._current_run
