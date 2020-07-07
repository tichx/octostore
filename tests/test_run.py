from time import time
import pytest
import json
import sys
import os
from pathlib import Path
import uuid
from opentelemetry.trace import Tracer, Span

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from octostore.run import Run  # noqa
from octostore.workflow import Workflow


def test_create_run():
    workflow_object = Workflow("DUMMY WORKFLOW NAME")
    run_id = str(uuid.uuid4().hex)
    this_run = Run(workflow_object, run_id=run_id)

    assert isinstance(this_run, Run)
    assert this_run.run_id == run_id
    assert isinstance(this_run.tracer, Tracer)


def test_start_run():
    workflow_object = Workflow("DUMMY WORKFLOW NAME")
    run_id = str(uuid.uuid4().hex)
    this_run = Run(workflow_object, run_id)
    this_run.start_run(time(), ['dummytag'])

    assert isinstance(this_run.root_span, Span)
    assert this_run.tags[0] == 'dummytag'
