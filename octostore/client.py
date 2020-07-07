import os
import sys
from pathlib import Path
from octostore.mongo_helper import MongoHelpers
from octostore.run import Run
from environs import Env

sys.path.append("..")
sys.path.append(str(Path(__file__).parent.resolve()))


class Client:
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

        self.mh = MongoHelpers(connection_uri)
        self.client = self.mh.get_client()
        self.db = self.client[db_name]
        self.user_collection = self.db["user"]

    def create_experiment(self, experiment_name, artifact_location) -> int:
        # TODO: ONLY writing artifact location to the cloud - ignoring other options for now
        return self.mh.create_experiment(experiment_name, None)

    def create_run(self, experiment_id, start_time, tags):
        self.current_run = Run(experiment_id=experiment_id, start_time=start_time, tags=tags)
        return self.current_run

    def get_current_run(self):
        return self.current_run
