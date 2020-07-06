import octostore
from octostore.mlflow.view_type import ViewType
from octostore.core import client

# Source: Name of the notebook that launched the run or the project name and entry point for the run.
# Version: Notebook revision if run from a notebook or Git commit hash if run from an MLflow Project.
# Start & end time: Start and end time of the run.
# Parameters: Key-value model parameters. Both keys and values are strings.
# Metrics: Key-value model evaluation metrics.The value is numeric. Each metric can be updated throughout the course of the run (for example, to track how your model’s loss function is converging), and MLflow records and lets you visualize the metric’s history.
# Tags: Key-value run metadata that can be updated during and after a run completes. Both keys and values are strings.
# Artifacts: Output files in any format. For example, you can record images, models (for example, a pickled scikit-learn model), and data files (for example, a Parquet file) as an artifact.

SEARCH_MAX_RESULTS_DEFAULT = 10000


class mlflow:
    """
    Client of an MLflow Tracking Server that creates and manages experiments and runs, and of an
    MLflow Registry Server that creates and manages registered models and model versions. It's a
    thin wrapper around TrackingServiceClient and RegistryClient so there is a unified API but we
    can keep the implementation of the tracking and registry clients independent from each other.
    """

    def __init__(self, registry_uri=None):
        # """
        # :param tracking_uri: Address of local or remote tracking server. If not provided, defaults
        #                      to the service set by ``mlflow.tracking.set_tracking_uri``. See
        #                      `Where Runs Get Recorded <../tracking.html#where-runs-get-recorded>`_
        #                      for more info.
        # :param registry_uri: Address of local or remote model registry server. If not provided,
        #                      defaults to the service set by ``mlflow.tracking.set_tracking_uri``.
        # """
        # final_tracking_uri = tracking_uri or utils.get_tracking_uri()
        # self._registry_uri = registry_uri or final_tracking_uri
        self._tracking_client = client()

        # `MlflowClient` also references a `ModelRegistryClient` instance that is provided by the
        # `MlflowClient._get_registry_client()` method. This `ModelRegistryClient` is not explicitly
        # defined as an instance variable in the `MlflowClient` constructor; an instance variable
        # is assigned lazily by `MlflowClient._get_registry_client()` and should not be referenced
        # outside of the `MlflowClient._get_registry_client()` method

    def get_run(self, run_id):
        """
        Fetch the run from backend store. The resulting :py:class:`Run <mlflow.entities.Run>`
        contains a collection of run metadata -- :py:class:`RunInfo <mlflow.entities.RunInfo>`,
        as well as a collection of run parameters, tags, and metrics --
        :py:class:`RunData <mlflow.entities.RunData>`. In the case where multiple metrics with the
        same key are logged for the run, the :py:class:`RunData <mlflow.entities.RunData>` contains
        the most recently logged value at the largest step for each metric.

        :param run_id: Unique identifier for the run.

        :return: A single :py:class:`mlflow.entities.Run` object, if the run exists. Otherwise,
                 raises an exception.
        """
        # return self._tracking_client.get_run(run_id)
        return NotImplementedError("NYI")

    def get_metric_history(self, run_id, key):
        """
        Return a list of metric objects corresponding to all values logged for a given metric.

        :param run_id: Unique identifier for run
        :param key: Metric name within the run

        :return: A list of :py:class:`mlflow.entities.Metric` entities if logged, else empty list
        """
        # return self._tracking_client.get_metric_history(run_id, key)
        return NotImplementedError("NYI")

    def create_run(self, experiment_id, start_time=None, tags=None):
        """
        Create a :py:class:`mlflow.entities.Run` object that can be associated with
        metrics, parameters, artifacts, etc.
        Unlike :py:func:`mlflow.projects.run`, creates objects but does not run code.
        Unlike :py:func:`mlflow.start_run`, does not change the "active run" used by
        :py:func:`mlflow.log_param`.

        :param experiment_id: The ID of then experiment to create a run in.
        :param start_time: If not provided, use the current timestamp.
        :param tags: A dictionary of key-value pairs that are converted into
                     :py:class:`mlflow.entities.RunTag` objects.
        :return: :py:class:`mlflow.entities.Run` that was created.
        """
        return self._tracking_client.create_run(experiment_id, start_time, tags)

    def list_run_infos(self, experiment_id, run_view_type=ViewType.ACTIVE_ONLY):
        """:return: List of :py:class:`mlflow.entities.RunInfo`"""
        # return self._tracking_client.list_run_infos(experiment_id, run_view_type)
        return NotImplementedError("NYI")

    def list_experiments(self, view_type=None):
        """
        :return: List of :py:class:`mlflow.entities.Experiment`
        """
        # return self._tracking_client.list_experiments(view_type)
        return NotImplementedError("NYI")

    def get_experiment(self, experiment_id):
        """
        Retrieve an experiment by experiment_id from the backend store

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        :return: :py:class:`mlflow.entities.Experiment`
        """
        # return self._tracking_client.get_experiment(experiment_id)
        return NotImplementedError("NYI")

    def get_experiment_by_name(self, name):
        """
        Retrieve an experiment by experiment name from the backend store

        :param name: The experiment name.
        :return: :py:class:`mlflow.entities.Experiment`
        """
        # return self._tracking_client.get_experiment_by_name(name)
        return NotImplementedError("NYI")

    def create_experiment(self, name, artifact_location=None):
        """Create an experiment.

        :param name: The experiment name. Must be unique.
        :param artifact_location: The location to store run artifacts.
                                  If not provided, the server picks an appropriate default.
        :return: Integer ID of the created experiment.
        """
        # return self._tracking_client.create_experiment(name, artifact_location)
        return NotImplementedError("NYI")

    def delete_experiment(self, experiment_id):
        """
        Delete an experiment from the backend store.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        # self._tracking_client.delete_experiment(experiment_id)
        return NotImplementedError("NYI")

    def restore_experiment(self, experiment_id):
        """
        Restore a deleted experiment unless permanently deleted.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        # self._tracking_client.restore_experiment(experiment_id)
        return NotImplementedError("NYI")

    def rename_experiment(self, experiment_id, new_name):
        """
        Update an experiment's name. The new name must be unique.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        # self._tracking_client.rename_experiment(experiment_id, new_name)
        return NotImplementedError("NYI")

    def log_metric(self, run_id, key, value, timestamp=None, step=None):
        """
        Log a metric against the run ID.

        :param run_id: The run id to which the metric should be logged.
        :param key: Metric name.
        :param value: Metric value (float). Note that some special values such
                      as +/- Infinity may be replaced by other values depending on the store. For
                      example, the SQLAlchemy store replaces +/- Inf with max / min float values.
        :param timestamp: Time when this metric was calculated. Defaults to the current system time.
        :param step: Integer training step (iteration) at which was the metric calculated.
                     Defaults to 0.
        """
        self._tracking_client.log_metric(run_id, key, value, timestamp, step)

    def log_param(self, run_id, key, value):
        """
        Log a parameter against the run ID. Value is converted to a string.
        """
        self._tracking_client.log_param(run_id, key, value)

    def set_experiment_tag(self, experiment_id, key, value):
        """
        Set a tag on the experiment with the specified ID. Value is converted to a string.

        :param experiment_id: String ID of the experiment.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string).
        """
        self._tracking_client.set_experiment_tag(experiment_id, key, value)

    def set_tag(self, run_id, key, value):
        """
        Set a tag on the run with the specified ID. Value is converted to a string.

        :param run_id: String ID of the run.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string)
        """
        self._tracking_client.set_tag(run_id, key, value)

    def delete_tag(self, run_id, key):
        """
        Delete a tag from a run. This is irreversible.

        :param run_id: String ID of the run
        :param key: Name of the tag
        """
        self._tracking_client.delete_tag(run_id, key)

    def log_batch(self, run_id, metrics=(), params=(), tags=()):
        """
        Log multiple metrics, params, and/or tags.

        :param run_id: String ID of the run
        :param metrics: If provided, List of Metric(key, value, timestamp) instances.
        :param params: If provided, List of Param(key, value) instances.
        :param tags: If provided, List of RunTag(key, value) instances.

        Raises an MlflowException if any errors occur.
        :return: None
        """
        # self._tracking_client.log_batch(run_id, metrics, params, tags)
        return NotImplementedError("NYI")

    def log_artifact(self, run_id, local_path, artifact_path=None):
        """
        Write a local file or directory to the remote ``artifact_uri``.

        :param local_path: Path to the file or directory to write.
        :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        self._tracking_client.log_artifact(run_id, local_path, artifact_path)

    def log_artifacts(self, run_id, local_dir, artifact_path=None):
        """
        Write a directory of files to the remote ``artifact_uri``.

        :param local_dir: Path to the directory of files to write.
        :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        self._tracking_client.log_artifacts(run_id, local_dir, artifact_path)

    def _record_logged_model(self, run_id, mlflow_model):
        """
        Record logged model info with the tracking server.

        :param run_id: run_id under which the model has been logged.
        :param mlflow_model: Model info to be recorded.
        """
        # self._tracking_client._record_logged_model(run_id, mlflow_model)
        return NotImplementedError("NYI")

    def list_artifacts(self, run_id, path=None):
        """
        List the artifacts for a run.

        :param run_id: The run to list artifacts from.
        :param path: The run's relative artifact path to list from. By default it is set to None
                     or the root artifact path.
        :return: List of :py:class:`mlflow.entities.FileInfo`
        """
        # return self._tracking_client.list_artifacts(run_id, path)
        return NotImplementedError("NYI")

    def download_artifacts(self, run_id, path, dst_path=None):
        """
        Download an artifact file or directory from a run to a local directory if applicable,
        and return a local path for it.

        :param run_id: The run to download artifacts from.
        :param path: Relative source path to the desired artifact.
        :param dst_path: Absolute path of the local filesystem destination directory to which to
                         download the specified artifacts. This directory must already exist.
                         If unspecified, the artifacts will either be downloaded to a new
                         uniquely-named directory on the local filesystem or will be returned
                         directly in the case of the LocalArtifactRepository.
        :return: Local path of desired artifact.
        """
        # return self._tracking_client.download_artifacts(run_id, path, dst_path)
        return NotImplementedError("NYI")

    def set_terminated(self, run_id, status=None, end_time=None):
        """Set a run's status to terminated.

        :param status: A string value of :py:class:`mlflow.entities.RunStatus`.
                       Defaults to "FINISHED".
        :param end_time: If not provided, defaults to the current time."""
        # self._tracking_client.set_terminated(run_id, status, end_time)
        return NotImplementedError("NYI")

    def delete_run(self, run_id):
        """
        Deletes a run with the given ID.
        """
        # self._tracking_client.delete_run(run_id)
        return NotImplementedError("NYI")

    def restore_run(self, run_id):
        """
        Restores a deleted run with the given ID.
        """
        # self._tracking_client.restore_run(run_id)
        return NotImplementedError("NYI")

    def search_runs(
        self,
        experiment_ids,
        filter_string="",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search experiments that fit the search criteria.

        :param experiment_ids: List of experiment IDs, or a single int or string id.
        :param filter_string: Filter query string, defaults to searching all runs.
        :param run_view_type: one of enum values ACTIVE_ONLY, DELETED_ONLY, or ALL runs
                              defined in :py:class:`mlflow.entities.ViewType`.
        :param max_results: Maximum number of runs desired.
        :param order_by: List of columns to order by (e.g., "metrics.rmse"). The ``order_by`` column
                     can contain an optional ``DESC`` or ``ASC`` value. The default is ``ASC``.
                     The default ordering is to sort by ``start_time DESC``, then ``run_id``.
        :param page_token: Token specifying the next page of results. It should be obtained from
            a ``search_runs`` call.

        :return: A list of :py:class:`mlflow.entities.Run` objects that satisfy the search
            expressions. If the underlying tracking store supports pagination, the token for
            the next page may be obtained via the ``token`` attribute of the returned object.
        """
        # return self._tracking_client.search_runs(experiment_ids, filter_string, run_view_type, max_results, order_by, page_token)
        return NotImplementedError("NYI")


# """
# Internal module implementing the fluent API, allowing management of an active
# MLflow run. This module is exposed to users at the top-level :py:mod:`mlflow` module.
# """
# import os

# import atexit
# import time
# import logging
# import numpy as np
# import pandas as pd

# from mlflow.entities import Run, RunStatus, Param, RunTag, Metric, ViewType
# from mlflow.entities.lifecycle_stage import LifecycleStage
# from mlflow.exceptions import MlflowException
# from mlflow.tracking.client import MlflowClient
# from mlflow.tracking import artifact_utils
# from mlflow.tracking.context import registry as context_registry
# from mlflow.utils import env
# from mlflow.utils.databricks_utils import is_in_databricks_notebook, get_notebook_id
# from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID, MLFLOW_RUN_NAME
# from mlflow.utils.validation import _validate_run_id

# _EXPERIMENT_ID_ENV_VAR = "MLFLOW_EXPERIMENT_ID"
# _EXPERIMENT_NAME_ENV_VAR = "MLFLOW_EXPERIMENT_NAME"
# _RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"
# _active_run_stack = []
# _active_experiment_id = None

# SEARCH_MAX_RESULTS_PANDAS = 100000
# NUM_RUNS_PER_PAGE_PANDAS = 10000

# _logger = logging.getLogger(__name__)


# def set_experiment(experiment_name):
#     """
#     Set given experiment as active experiment. If experiment does not exist, create an experiment
#     with provided name.

#     :param experiment_name: Name of experiment to be activated.
#     """
#     client = MlflowClient()
#     experiment = client.get_experiment_by_name(experiment_name)
#     exp_id = experiment.experiment_id if experiment else None
#     if exp_id is None:  # id can be 0
#         print("INFO: '{}' does not exist. Creating a new experiment".format(experiment_name))
#         exp_id = client.create_experiment(experiment_name)
#     elif experiment.lifecycle_stage == LifecycleStage.DELETED:
#         raise MlflowException(
#             "Cannot set a deleted experiment '%s' as the active experiment."
#             " You can restore the experiment, or permanently delete the "
#             " experiment to create a new one." % experiment.name)
#     global _active_experiment_id
#     _active_experiment_id = exp_id


# class ActiveRun(Run):  # pylint: disable=W0223
#     """Wrapper around :py:class:`mlflow.entities.Run` to enable using Python ``with`` syntax."""

#     def __init__(self, run):
#         Run.__init__(self, run.info, run.data)

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
#         end_run(RunStatus.to_string(status))
#         return exc_type is None


# def start_run(run_id=None, experiment_id=None, run_name=None, nested=False):
#     """
#     Start a new MLflow run, setting it as the active run under which metrics and parameters
#     will be logged. The return value can be used as a context manager within a ``with`` block;
#     otherwise, you must call ``end_run()`` to terminate the current run.

#     If you pass a ``run_id`` or the ``MLFLOW_RUN_ID`` environment variable is set,
#     ``start_run`` attempts to resume a run with the specified run ID and
#     other parameters are ignored. ``run_id`` takes precedence over ``MLFLOW_RUN_ID``.

#     MLflow sets a variety of default tags on the run, as defined in
#     :ref:`MLflow system tags <system_tags>`.

#     :param run_id: If specified, get the run with the specified UUID and log parameters
#                      and metrics under that run. The run's end time is unset and its status
#                      is set to running, but the run's other attributes (``source_version``,
#                      ``source_type``, etc.) are not changed.
#     :param experiment_id: ID of the experiment under which to create the current run (applicable
#                           only when ``run_id`` is not specified). If ``experiment_id`` argument
#                           is unspecified, will look for valid experiment in the following order:
#                           activated using ``set_experiment``, ``MLFLOW_EXPERIMENT_NAME``
#                           environment variable, ``MLFLOW_EXPERIMENT_ID`` environment variable,
#                           or the default experiment as defined by the tracking server.
#     :param run_name: Name of new run (stored as a ``mlflow.runName`` tag).
#                      Used only when ``run_id`` is unspecified.
#     :param nested: Controls whether run is nested in parent run. ``True`` creates a nest run.
#     :return: :py:class:`mlflow.ActiveRun` object that acts as a context manager wrapping
#              the run's state.
#     """
#     global _active_run_stack
#     # back compat for int experiment_id
#     experiment_id = str(experiment_id) if isinstance(experiment_id, int) else experiment_id
#     if len(_active_run_stack) > 0 and not nested:
#         raise Exception(("Run with UUID {} is already active. To start a new run, first end the " +
#                          "current run with mlflow.end_run(). To start a nested " +
#                          "run, call start_run with nested=True").format(
#             _active_run_stack[0].info.run_id))
#     if run_id:
#         existing_run_id = run_id
#     elif _RUN_ID_ENV_VAR in os.environ:
#         existing_run_id = os.environ[_RUN_ID_ENV_VAR]
#         del os.environ[_RUN_ID_ENV_VAR]
#     else:
#         existing_run_id = None
#     if existing_run_id:
#         _validate_run_id(existing_run_id)
#         active_run_obj = MlflowClient().get_run(existing_run_id)
#         # Check to see if experiment_id from environment matches experiment_id from set_experiment()
#         if (_active_experiment_id is not None and
#                 _active_experiment_id != active_run_obj.info.experiment_id):
#             raise MlflowException("Cannot start run with ID {} because active run ID "
#                                   "does not match environment run ID. Make sure --experiment-name "
#                                   "or --experiment-id matches experiment set with "
#                                   "set_experiment(), or just use command-line "
#                                   "arguments".format(existing_run_id))
#         # Check to see if current run isn't deleted
#         if active_run_obj.info.lifecycle_stage == LifecycleStage.DELETED:
#             raise MlflowException("Cannot start run with ID {} because it is in the "
#                                   "deleted state.".format(existing_run_id))
#     else:
#         if len(_active_run_stack) > 0:
#             parent_run_id = _active_run_stack[-1].info.run_id
#         else:
#             parent_run_id = None

#         exp_id_for_run = experiment_id if experiment_id is not None else _get_experiment_id()

#         user_specified_tags = {}
#         if parent_run_id is not None:
#             user_specified_tags[MLFLOW_PARENT_RUN_ID] = parent_run_id
#         if run_name is not None:
#             user_specified_tags[MLFLOW_RUN_NAME] = run_name

#         tags = context_registry.resolve_tags(user_specified_tags)

#         active_run_obj = MlflowClient().create_run(
#             experiment_id=exp_id_for_run,
#             tags=tags
#         )

#     _active_run_stack.append(ActiveRun(active_run_obj))
#     return _active_run_stack[-1]


# def end_run(status=RunStatus.to_string(RunStatus.FINISHED)):
#     """End an active MLflow run (if there is one)."""
#     global _active_run_stack
#     if len(_active_run_stack) > 0:
#         # Clear out the global existing run environment variable as well.
#         env.unset_variable(_RUN_ID_ENV_VAR)
#         run = _active_run_stack.pop()
#         MlflowClient().set_terminated(run.info.run_id, status)


# atexit.register(end_run)


# def active_run():
#     """Get the currently active ``Run``, or None if no such run exists.

#     **Note**: You cannot access currently-active run attributes
#     (parameters, metrics, etc.) through the run returned by ``mlflow.active_run``. In order
#     to access such attributes, use the :py:class:`mlflow.tracking.MlflowClient` as follows:

#     .. code-block:: py

#         client = mlflow.tracking.MlflowClient()
#         data = client.get_run(mlflow.active_run().info.run_id).data
#     """
#     return _active_run_stack[-1] if len(_active_run_stack) > 0 else None


# def get_run(run_id):
#     """
#     Fetch the run from backend store. The resulting :py:class:`Run <mlflow.entities.Run>`
#     contains a collection of run metadata -- :py:class:`RunInfo <mlflow.entities.RunInfo>`,
#     as well as a collection of run parameters, tags, and metrics --
#     :py:class:`RunData <mlflow.entities.RunData>`. In the case where multiple metrics with the
#     same key are logged for the run, the :py:class:`RunData <mlflow.entities.RunData>` contains
#     the most recently logged value at the largest step for each metric.

#     :param run_id: Unique identifier for the run.

#     :return: A single :py:class:`mlflow.entities.Run` object, if the run exists. Otherwise,
#                 raises an exception.
#     """
#     return MlflowClient().get_run(run_id)


# def log_param(key, value):
#     """
#     Log a parameter under the current run. If no run is active, this method will create
#     a new active run.

#     :param key: Parameter name (string)
#     :param value: Parameter value (string, but will be string-ified if not)
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().log_param(run_id, key, value)


# def set_tag(key, value):
#     """
#     Set a tag under the current run. If no run is active, this method will create a
#     new active run.

#     :param key: Tag name (string)
#     :param value: Tag value (string, but will be string-ified if not)
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().set_tag(run_id, key, value)


# def delete_tag(key):
#     """
#     Delete a tag from a run. This is irreversible. If no run is active, this method
#     will create a new active run.

#     :param key: Name of the tag
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().delete_tag(run_id, key)


# def log_metric(key, value, step=None):
#     """
#     Log a metric under the current run. If no run is active, this method will create
#     a new active run.

#     :param key: Metric name (string).
#     :param value: Metric value (float). Note that some special values such as +/- Infinity may be
#                   replaced by other values depending on the store. For example, sFor example, the
#                   SQLAlchemy store replaces +/- Inf with max / min float values.
#     :param step: Metric step (int). Defaults to zero if unspecified.
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().log_metric(run_id, key, value, int(time.time() * 1000), step or 0)


# def log_metrics(metrics, step=None):
#     """
#     Log multiple metrics for the current run. If no run is active, this method will create a new
#     active run.

#     :param metrics: Dictionary of metric_name: String -> value: Float. Note that some special values
#                     such as +/- Infinity may be replaced by other values depending on the store.
#                     For example, sql based store may replace +/- Inf with max / min float values.
#     :param step: A single integer step at which to log the specified
#                  Metrics. If unspecified, each metric is logged at step zero.

#     :returns: None
#     """
#     run_id = _get_or_start_run().info.run_id
#     timestamp = int(time.time() * 1000)
#     metrics_arr = [Metric(key, value, timestamp, step or 0) for key, value in metrics.items()]
#     MlflowClient().log_batch(run_id=run_id, metrics=metrics_arr, params=[], tags=[])


# def log_params(params):
#     """
#     Log a batch of params for the current run. If no run is active, this method will create a
#     new active run.

#     :param params: Dictionary of param_name: String -> value: (String, but will be string-ified if
#                    not)
#     :returns: None
#     """
#     run_id = _get_or_start_run().info.run_id
#     params_arr = [Param(key, str(value)) for key, value in params.items()]
#     MlflowClient().log_batch(run_id=run_id, metrics=[], params=params_arr, tags=[])


# def set_tags(tags):
#     """
#     Log a batch of tags for the current run. If no run is active, this method will create a
#     new active run.

#     :param tags: Dictionary of tag_name: String -> value: (String, but will be string-ified if
#                  not)
#     :returns: None
#     """
#     run_id = _get_or_start_run().info.run_id
#     tags_arr = [RunTag(key, str(value)) for key, value in tags.items()]
#     MlflowClient().log_batch(run_id=run_id, metrics=[], params=[], tags=tags_arr)


# def log_artifact(local_path, artifact_path=None):
#     """
#     Log a local file or directory as an artifact of the currently active run. If no run is
#     active, this method will create a new active run.

#     :param local_path: Path to the file to write.
#     :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().log_artifact(run_id, local_path, artifact_path)


# def log_artifacts(local_dir, artifact_path=None):
#     """
#     Log all the contents of a local directory as artifacts of the run. If no run is active,
#     this method will create a new active run.

#     :param local_dir: Path to the directory of files to write.
#     :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
#     """
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient().log_artifacts(run_id, local_dir, artifact_path)


# def _record_logged_model(mlflow_model):
#     run_id = _get_or_start_run().info.run_id
#     MlflowClient()._record_logged_model(run_id, mlflow_model)


# def get_experiment(experiment_id):
#     """
#     Retrieve an experiment by experiment_id from the backend store

#     :param experiment_id: The experiment ID returned from ``create_experiment``.
#     :return: :py:class:`mlflow.entities.Experiment`
#     """
#     return MlflowClient().get_experiment(experiment_id)


# def get_experiment_by_name(name):
#     """
#     Retrieve an experiment by experiment name from the backend store

#     :param name: The experiment name.
#     :return: :py:class:`mlflow.entities.Experiment`
#     """
#     return MlflowClient().get_experiment_by_name(name)


# def create_experiment(name, artifact_location=None):
#     """
#     Create an experiment.

#     :param name: The experiment name. Must be unique.
#     :param artifact_location: The location to store run artifacts.
#                               If not provided, the server picks an appropriate default.
#     :return: Integer ID of the created experiment.
#     """
#     return MlflowClient().create_experiment(name, artifact_location)


# def delete_experiment(experiment_id):
#     """
#     Delete an experiment from the backend store.

#     :param experiment_id: The experiment ID returned from ``create_experiment``.
#     """
#     MlflowClient().delete_experiment(experiment_id)


# def delete_run(run_id):
#     """
#     Deletes a run with the given ID.

#     :param run_id: Unique identifier for the run to delete.
#     """
#     MlflowClient().delete_run(run_id)


# def get_artifact_uri(artifact_path=None):
#     """
#     Get the absolute URI of the specified artifact in the currently active run.
#     If `path` is not specified, the artifact root URI of the currently active
#     run will be returned; calls to ``log_artifact`` and ``log_artifacts`` write
#     artifact(s) to subdirectories of the artifact root URI.

#     If no run is active, this method will create a new active run.

#     :param artifact_path: The run-relative artifact path for which to obtain an absolute URI.
#                           For example, "path/to/artifact". If unspecified, the artifact root URI
#                           for the currently active run will be returned.
#     :return: An *absolute* URI referring to the specified artifact or the currently adtive run's
#              artifact root. For example, if an artifact path is provided and the currently active
#              run uses an S3-backed store, this may be a uri of the form
#              ``s3://<bucket_name>/path/to/artifact/root/path/to/artifact``. If an artifact path
#              is not provided and the currently active run uses an S3-backed store, this may be a
#              URI of the form ``s3://<bucket_name>/path/to/artifact/root``.
#     """
#     return artifact_utils.get_artifact_uri(run_id=_get_or_start_run().info.run_id,
#                                            artifact_path=artifact_path)


# def search_runs(experiment_ids=None, filter_string="", run_view_type=ViewType.ACTIVE_ONLY,
#                 max_results=SEARCH_MAX_RESULTS_PANDAS, order_by=None):
#     """
#     Get a pandas DataFrame of runs that fit the search criteria.

#     :param experiment_ids: List of experiment IDs. None will default to the active experiment.
#     :param filter_string: Filter query string, defaults to searching all runs.
#     :param run_view_type: one of enum values ``ACTIVE_ONLY``, ``DELETED_ONLY``, or ``ALL`` runs
#                             defined in :py:class:`mlflow.entities.ViewType`.
#     :param max_results: The maximum number of runs to put in the dataframe. Default is 100,000
#                         to avoid causing out-of-memory issues on the user's machine.
#     :param order_by: List of columns to order by (e.g., "metrics.rmse"). The ``order_by`` column
#                      can contain an optional ``DESC`` or ``ASC`` value. The default is ``ASC``.
#                      The default ordering is to sort by ``start_time DESC``, then ``run_id``.

#     :return: A pandas.DataFrame of runs, where each metric, parameter, and tag
#         are expanded into their own columns named metrics.*, params.*, and tags.*
#         respectively. For runs that don't have a particular metric, parameter, or tag, their
#         value will be (NumPy) Nan, None, or None respectively.
#     """
#     if not experiment_ids:
#         experiment_ids = _get_experiment_id()
#     runs = _get_paginated_runs(experiment_ids, filter_string, run_view_type, max_results,
#                                order_by)
#     info = {'run_id': [], 'experiment_id': [],
#             'status': [], 'artifact_uri': [],
#             'start_time': [], 'end_time': []}
#     params, metrics, tags = ({}, {}, {})
#     PARAM_NULL, METRIC_NULL, TAG_NULL = (None, np.nan, None)
#     for i, run in enumerate(runs):
#         info['run_id'].append(run.info.run_id)
#         info['experiment_id'].append(run.info.experiment_id)
#         info['status'].append(run.info.status)
#         info['artifact_uri'].append(run.info.artifact_uri)
#         info['start_time'].append(pd.to_datetime(run.info.start_time, unit="ms", utc=True))
#         info['end_time'].append(pd.to_datetime(run.info.end_time, unit="ms", utc=True))

#         # Params
#         param_keys = set(params.keys())
#         for key in param_keys:
#             if key in run.data.params:
#                 params[key].append(run.data.params[key])
#             else:
#                 params[key].append(PARAM_NULL)
#         new_params = set(run.data.params.keys()) - param_keys
#         for p in new_params:
#             params[p] = [PARAM_NULL]*i  # Fill in null values for all previous runs
#             params[p].append(run.data.params[p])

#         # Metrics
#         metric_keys = set(metrics.keys())
#         for key in metric_keys:
#             if key in run.data.metrics:
#                 metrics[key].append(run.data.metrics[key])
#             else:
#                 metrics[key].append(METRIC_NULL)
#         new_metrics = set(run.data.metrics.keys()) - metric_keys
#         for m in new_metrics:
#             metrics[m] = [METRIC_NULL]*i
#             metrics[m].append(run.data.metrics[m])

#         # Tags
#         tag_keys = set(tags.keys())
#         for key in tag_keys:
#             if key in run.data.tags:
#                 tags[key].append(run.data.tags[key])
#             else:
#                 tags[key].append(TAG_NULL)
#         new_tags = set(run.data.tags.keys()) - tag_keys
#         for t in new_tags:
#             tags[t] = [TAG_NULL]*i
#             tags[t].append(run.data.tags[t])

#     data = {}
#     data.update(info)
#     for key in metrics:
#         data['metrics.' + key] = metrics[key]
#     for key in params:
#         data['params.' + key] = params[key]
#     for key in tags:
#         data['tags.' + key] = tags[key]
#     return pd.DataFrame(data)


# def _get_paginated_runs(experiment_ids, filter_string, run_view_type, max_results,
#                         order_by):
#     all_runs = []
#     next_page_token = None
#     while(len(all_runs) < max_results):
#         runs_to_get = max_results-len(all_runs)
#         if runs_to_get < NUM_RUNS_PER_PAGE_PANDAS:
#             runs = MlflowClient().search_runs(experiment_ids, filter_string, run_view_type,
#                                               runs_to_get, order_by, next_page_token)
#         else:
#             runs = MlflowClient().search_runs(experiment_ids, filter_string, run_view_type,
#                                               NUM_RUNS_PER_PAGE_PANDAS, order_by, next_page_token)
#         all_runs.extend(runs)
#         if hasattr(runs, 'token') and runs.token != '' and runs.token is not None:
#             next_page_token = runs.token
#         else:
#             break
#     return all_runs


# def _get_or_start_run():
#     if len(_active_run_stack) > 0:
#         return _active_run_stack[-1]
#     return start_run()


# def _get_experiment_id_from_env():
#     experiment_name = env.get_env(_EXPERIMENT_NAME_ENV_VAR)
#     if experiment_name is not None:
#         exp = MlflowClient().get_experiment_by_name(experiment_name)
#         return exp.experiment_id if exp else None
#     return env.get_env(_EXPERIMENT_ID_ENV_VAR)


# def _get_experiment_id():
#     # TODO: Replace with None for 1.0, leaving for 0.9.1 release backcompat with existing servers
#     deprecated_default_exp_id = "0"

#     return (_active_experiment_id or
#             _get_experiment_id_from_env() or
#             (is_in_databricks_notebook() and get_notebook_id())) or deprecated_default_exp_id


# global _active_run_stack
# # back compat for int experiment_id
# experiment_id = str(experiment_id) if isinstance(experiment_id, int) else experiment_id
# if len(_active_run_stack) > 0 and not nested:
#     raise Exception(("Run with UUID {} is already active. To start a new run, first end the " +
#                      "current run with mlflow.end_run(). To start a nested " +
#                      "run, call start_run with nested=True").format(
#         _active_run_stack[0].info.run_id))
# if run_id:
#     existing_run_id = run_id
# elif _RUN_ID_ENV_VAR in os.environ:
#     existing_run_id = os.environ[_RUN_ID_ENV_VAR]
#     del os.environ[_RUN_ID_ENV_VAR]
# else:
#     existing_run_id = None
# if existing_run_id:
#     _validate_run_id(existing_run_id)
#     active_run_obj = MlflowClient().get_run(existing_run_id)
#     # Check to see if experiment_id from environment matches experiment_id from set_experiment()
#     if (_active_experiment_id is not None and
#             _active_experiment_id != active_run_obj.info.experiment_id):
#         raise MlflowException("Cannot start run with ID {} because active run ID "
#                               "does not match environment run ID. Make sure --experiment-name "
#                               "or --experiment-id matches experiment set with "
#                               "set_experiment(), or just use command-line "
#                               "arguments".format(existing_run_id))
#     # Check to see if current run isn't deleted
#     if active_run_obj.info.lifecycle_stage == LifecycleStage.DELETED:
#         raise MlflowException("Cannot start run with ID {} because it is in the "
#                               "deleted state.".format(existing_run_id))
# else:
#     if len(_active_run_stack) > 0:
#         parent_run_id = _active_run_stack[-1].info.run_id
#     else:
#         parent_run_id = None

#     exp_id_for_run = experiment_id if experiment_id is not None else _get_experiment_id()

#     user_specified_tags = {}
#     if parent_run_id is not None:
#         user_specified_tags[MLFLOW_PARENT_RUN_ID] = parent_run_id
#     if run_name is not None:
#         user_specified_tags[MLFLOW_RUN_NAME] = run_name

#     tags = context_registry.resolve_tags(user_specified_tags)

#     active_run_obj = MlflowClient().create_run(
#         experiment_id=exp_id_for_run,
#         tags=tags
#     )

# _active_run_stack.append(ActiveRun(active_run_obj))
# return _active_run_stack[-1]
