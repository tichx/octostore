from octostore.workflow import Workflow
import pytest
import json
import sys
import os
from pathlib import Path
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_create_workflow():
    workflow_name = "DUMMY WORKFLOW NAME"
    this_workflow = Workflow(workflow_name)

    assert this_workflow.workflow_name == workflow_name
