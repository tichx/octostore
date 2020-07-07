from octostore.mlflow.entities.lifecycle_stage import LifecycleStage
from octostore.mlflow.protos.service_pb2 import Experiment
from pymongo import MongoClient
import os
import sys
from pathlib import Path
from environs import Env
from octostore.entities.view_type import ViewType
from octostore.entities.experiment import Experiment

sys.path.append("..")
sys.path.append(str(Path(__file__).parent.resolve()))


class MongoHelpers:
    _client = None
    _db = None
    _collection = None

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

        self.client = MongoClient(connection_uri)
        self.db = self._client[db_name]

    def create_experiment(self, name, artifact_location=None, tags=[]):
        # all_experiments = self.get_all_experiments()
        # Get all existing experiments and find the one with largest numerical ID.
        # len(list_all(..)) would not work when experiments are deleted.
        # experiments_ids = [
        #     int(e.experiment_id)
        #     for e in self.list_experiments(ViewType.ALL)
        #     if e.experiment_id.isdigit()
        # ]
        experiment_id = self._get_highest_experiment_id() + 1
        return self._create_experiment_with_id(name, str(experiment_id), artifact_location, tags)

    def _create_experiment_with_id(self, experiment_name, experiment_id, artifact_location, lifecycle_stage: LifecycleStage = LifecycleStage.ACTIVE, tags=[]) -> int:
        e = Experiment(experiment_id, experiment_name, experiment_id, artifact_location, lifecycle_stage, tags)

    def _get_highest_experiment_id(self):
        if len(list(self._client.experiments.find())) is not 0:
            last_experiment = list(self.db.experiments.find({}).sort("experiment_id", -1).limit(1))
            return last_experiment[0]["experiment_id"]
        else:
            return 0

    def list_experiments(self, view_type=ViewType.ACTIVE_ONLY):
        rsl = []
        if view_type == ViewType.ACTIVE_ONLY or view_type == ViewType.ALL:
            rsl += self._get_active_experiments(full_path=False)
        if view_type == ViewType.DELETED_ONLY or view_type == ViewType.ALL:
            # rsl += self._get_deleted_experiments(full_path=False)
            pass
        experiments = []
        for exp_id in rsl:
            try:
                # trap and warn known issues, will raise unexpected exceptions to caller
                experiment = self._get_experiment(exp_id, view_type)
                if experiment:
                    experiments.append(experiment)
            except MissingConfigException as rnfe:
                # Trap malformed experiments and log warnings.
                logging.warning("Malformed experiment '%s'. Detailed error %s",
                                str(exp_id), str(rnfe), exc_info=True)
        return experiments

    def _get_active_experiments(self, full_path=False):
        active_experiments_query = {"type": "experiment", "experiment_state": LifecycleStage.ACTIVE}

        all_experiments = self.db.experiments.find(active_experiments_query)
        # exp_list = list_subdirs(self.root_directory, full_path)
        # return [exp for exp in exp_list if not exp.endswith(FileStore.TRASH_FOLDER_NAME)]

    def _get_deleted_experiments(self, full_path=False):
        # return list_subdirs(self.trash_folder, full_path)
        raise NotImplementedError("get_deleted_experiments")