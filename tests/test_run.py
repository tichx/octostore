import pytest
import json
import sys
import os
from pathlib import Path
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from octostore.run import Run  # noqa


def test_create_run():
    run_id = str(uuid.uuid4().hex)
    this_run = Run(experiment_id="DUMMY_EXPERIMENT_ID", run_id=run_id)

    assert isinstance(this_run, Run)
    assert this_run.current_run.instrumentation_info.name.startswith(run_id)


def test_start_run():
    run_id = str(uuid.uuid4().hex)
    this_run = Run(experiment_id="DUMMY_EXPERIMENT_ID", run_id=run_id)
    this_run.start_run()

    assert this_run.current_span is not None
