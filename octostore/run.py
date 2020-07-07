# ~/*
#  * Copyright 2018 Databricks, Inc.  All rights reserved.
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  * http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  *
#  * Modifitations - David Aronchick <david.aronchick@microsoft.com>
#  *
#  */

from octostore.exceptions import OctostoreException
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.trace import Tracer
from opentelemetry.trace import Span

from tempfile import gettempdir

import datetime
from pathlib import Path
import uuid
import yaml as YAML
import time
import math

from octostore.entities.source_type import SourceType
from octostore.entities.run_status import RunStatus
from octostore.entities.lifecycle_stage import LifecycleStage
from octostore.entities.run_tag import RunTag
from octostore.entities.run_info import RunInfo


class FileStore:
    TRASH_FOLDER_NAME = ".trash"
    ARTIFACTS_FOLDER_NAME = "artifacts"
    METRICS_FOLDER_NAME = "metrics"
    PARAMS_FOLDER_NAME = "params"
    TAGS_FOLDER_NAME = "tags"
    EXPERIMENT_TAGS_FOLDER_NAME = "tags"
    RESERVED_EXPERIMENT_FOLDERS = [EXPERIMENT_TAGS_FOLDER_NAME]
    META_DATA_FILE_NAME = "meta.yaml"
    DEFAULT_EXPERIMENT_ID = "0"


class Run:
    _dummy_user_id = "I_AM_A_DUMMY_USER_ID"

    def __init__(self, experiment_id, run_id: str = None, tags: list = [], start_time: datetime = None):
        """
        Creates a run with the specified attributes.
        """
        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )
        start_time = start_time or time.time()

        # TODO: Look up how MLFlow creates unique run names
        run_id = run_id or f"{experiment_id}-{math.floor(start_time)}"

        # experiment = self.get_experiment(experiment_id)
        # if experiment is None:
        #     raise MlflowException(
        #         "Could not create run under experiment with ID %s - no such experiment "
        #         "exists." % experiment_id,
        #         databricks_pb2.RESOURCE_DOES_NOT_EXIST)
        # if experiment.lifecycle_stage != LifecycleStage.ACTIVE:
        #     raise MlflowException(
        #         "Could not create run under non-active experiment with ID "
        #         "%s." % experiment_id,
        #         databricks_pb2.INVALID_STATE)
        run_uuid = uuid.uuid4().hex

        # TODO: Allow different directories
        # artifact_uri = self._get_artifact_dir(experiment_id, run_uuid)
        tmpdir = gettempdir()
        octostore_tmpdir = Path(tmpdir) / "octostore_tmp"
        if not octostore_tmpdir.exists():
            Path.mkdir(octostore_tmpdir)

        experiment_metrics_dir = octostore_tmpdir / str(experiment_id)
        if not experiment_metrics_dir.exists():
            Path.mkdir(experiment_metrics_dir)

        run_metrics_dir = experiment_metrics_dir / str(run_id)
        if not run_metrics_dir.exists():
            Path.mkdir(run_metrics_dir)

        artifact_uri = run_metrics_dir

        run_info = RunInfo(
            run_uuid=run_uuid,
            run_id=run_uuid,
            experiment_id=str(experiment_id),
            artifact_uri=str(artifact_uri),
            user_id=self._dummy_user_id,
            status=RunStatus.to_string(RunStatus.RUNNING),
            start_time=start_time,
            end_time=None,
            lifecycle_stage=LifecycleStage.ACTIVE,
        )
        # Persist run metadata and create directories for logging metrics, parameters, artifacts
        # run_dir = self._get_run_dir(run_info.experiment_id, run_info.run_id)
        # mkdir(run_dir)
        # Just doing the assignment below for compatibility
        run_dir = run_metrics_dir

        run_info_dict = Run._make_persisted_run_info_dict(run_info)
        (Path(run_dir) / FileStore.META_DATA_FILE_NAME).write_text(
            YAML.safe_dump(run_info_dict)
        )
        Path.mkdir(run_dir / FileStore.METRICS_FOLDER_NAME)
        Path.mkdir(run_dir / FileStore.PARAMS_FOLDER_NAME)
        Path.mkdir(run_dir / FileStore.ARTIFACTS_FOLDER_NAME)

        self.tags = []
        for tag in tags:
            self.set_tag(run_uuid, tag)

        self.current_run = trace.get_tracer(run_id)
        self.run_id = run_id
        self.experiment_id = experiment_id
        self.current_span = None
        self.start_time = start_time
        self.user_id = self._dummy_user_id


    @staticmethod
    def _make_persisted_run_info_dict(run_info):
        # 'tags' was moved from RunInfo to RunData, so we must keep storing it in the meta.yaml for
        # old mlflow versions to read
        run_info_dict = dict(run_info)
        run_info_dict["tags"] = []
        run_info_dict["name"] = ""
        if "status" in run_info_dict:
            # 'status' is stored as an integer enum in meta file, but RunInfo.status field is a string.
            # Convert from string to enum/int before storing.
            run_info_dict["status"] = RunStatus.from_string(run_info.status)
        else:
            run_info_dict["status"] = RunStatus.RUNNING
        run_info_dict["source_type"] = SourceType.LOCAL
        run_info_dict["source_name"] = ""
        run_info_dict["entry_point_name"] = ""
        run_info_dict["source_version"] = ""
        return run_info_dict

    def start_run(self, start_time=None, tags=[]):
        self.current_run.start_as_current_span(self.run_id)
        self.current_span = self.current_run.CURRENT_SPAN
        self.current_span.set_attribute(
            "start_time", start_time or datetime.datetime.now().isoformat
        )
        self.current_span.set_attribute(
            "start_time", start_time or datetime.datetime.now().isoformat
        )
        self.current_span.set_attribute("tags", tags)
        return self.current_run

    def start_span(self, span_name: str):
        self.current_span = self.current_run.start_as_current_span(span_name)
        return self.current_span

    def set_tag(self, key, value):
        """
        Set a tag on the run with the specified ID. Value is converted to a string.
        :param run_id: String ID of the run.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string)
        """
        tag = RunTag(key, str(value))
        self.tags.append(tag)


def check_run_is_active(run_info):
    if run_info.lifecycle_stage != LifecycleStage.ACTIVE:
        raise OctostoreException(
            "The run {} must be in 'active' lifecycle_stage.".format(run_info.run_id)
        )


def check_run_is_deleted(run_info):
    if run_info.lifecycle_stage != LifecycleStage.DELETED:
        raise OctostoreException(
            "The run {} must be in 'deleted' lifecycle_stage.".format(run_info.run_id)
        )


class searchable_attribute(property):
    # Wrapper class over property to designate some of the properties as searchable
    # run attributes
    pass


class orderable_attribute(property):
    # Wrapper class over property to designate some of the properties as orderable
    # run attributes
    pass

