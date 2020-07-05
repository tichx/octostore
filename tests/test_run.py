import pytest
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from octostore.run import Run  # noqa


def test_create_run():
    run_name = "test_run"
    this_run = Run(run_name)

    assert isinstance(this_run, Run)
    assert this_run.get_current_run().instrumentation_info.name == run_name


def test_start_run():
    this_run = Run("test_run")
    this_run.start_run()

    assert this_run.get_current_span() is not None
