# -*- coding: utf-8 -*-
from . import helpers
from octostore.run import Run


def client(run_name: str = None) -> Run:
    return Run(run_name)


def create_workflow():
    """Get a thought."""
    return "hmmm..."


# def hmm():
#     """Contemplation..."""
#     if helpers.get_answer():
#         print(get_hmm())
