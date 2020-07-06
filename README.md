# Octostore 

A core issue with workflows of ALL types today is the lack of a clean way to reason about them as a series of connected steps. Part of the issue is that each step is responsible for reading and writing its own information about execution, and there is no universal layer to integrate all the metadata together.

A simple 'job to be done' which is very difficult today is:
- In order for a developer to make decisions about the health of a component, she needs to compare every aspect of my previous workflow runs, and trivially compare them with runs that the current component out in production.

In order to do so, today, a developer would need to have:
- Figure out how to read and write to an metadata type (text? yaml? json?)
- Verify they CRUD'd the metadata correctly
- Instrument their code with custom functions for reading and writing the information
- Parse through log blobs which have no awareness of metadata in order to centralize results
- Use a store (e.g. keyvalue store, etc) which has no awareness of metadata or how the steps are tied together
- Build a system for CRUD-ing metadata in a unified way (e.g. give me all the metadata related to this workflow run, store all the metadata i'm giving you as independent elements that are tied together)
- And so on

Our goal is to enable the job to be done in the simplest possible way so that developers can read/write to the store and make better decisions about what to focus on to make their customers happier. 

A sample code blurb for how this might work follows:
```python
import github.octostore

# Create workflow
workflow_DAG = """
worflow:
    step_one:
        previous: None
        spec: step_one_spec
        next: step_two
    step_two:
        previous: step_one
        spec: step_two_spec
        next: step_three
    step_three:
        previous: step_two
        spec: step_three_spec
        next: None
"""
workflow_object = octostore.create_workflow(workflow_DAG) # Octostore "workflow" object

# Create specific run
this_run = workflow_object.create_run()

# Workflow step 1
workflow_object_step_one = run_workflow_step(parameters_for_step_one)
this_run.attach(workflow_object_step_one)

# Workflow step 2
workflow_object_step_two = run_workflow_step(parameters_for_step_two)
workflow_object_step_two.field_that_expects_int = "INVALID STRING"
workflow_object_step_two.field_that_is_required = None

this_run.attach(workflow_object_step_two) # <= returns " {field_that_expects_int: 'expects 'int', but was provided 'string': "INVALID STRING", field_that_is_required: 'may not be null'}
workflow_object_step_two.field_that_expects_int = 1.0
workflow_object_step_two.field_that_is_required = "value"
this_run.attach(workflow_object_step_two) # <= works correctly

# Workflow step 3
workflow_object_step_three = run_workflow_step(parameters_for_step_three)
this_run.attach(workflow_object_step_three)

# Save the run
wf_run_id = this_run.save()
print(f"Workflow Run ID: {wf_run_id}") # Outputs a unique ID for the workflow run that I can use to load at any time

# Load an arbitrary workflow
old_workflow_run = octostore.load_workflow_run('8ca59280-931e-49f2-9be8-9f5612f77620') # Unique WF ID
print(f"Results from step_one output in JSON: '{old_workflow_run.workflow_step_one.output.to_json()}")

# Diff between two workflows:
octostore.diff(old_workflow_run, this_run)  # Outputs a clean lists of diffs

# All results in the last two weeks
octostore.get_all_runs(date_one=datetime.datetime.now(), date_two=(datetime.datetime.now().timedelta(days = 14)))
```

This project is about building an API to enable the above scenarios.

Things we are NOT inventing:
- A schema definition language - we're using OpenAPI/Proto
- A schema validator - we're using Marshmallow/OpenAPI/Proto
- A key-value store - we're using CosmoDB/etc
- A workflow definition language - we're using OpenAPI
- A dashboard for displaying - that's ObservableHQ & PowerBI
- ...

We ARE inventing a SIMPLE, WELL-INTEGRATED SDK that ties them together that says:
- Here this thing
- Validate this thing
- Store this thing
- Give me a bunch of these things back in the future
- Compare thing A to thing B

Future investments
After we do the above, priority one will be to build automated adapters to pull in from common, opaque sources today - for example, web server logs, kubernetes logs, event streams, blah. We will also provide a system to allow you to extend these adapters using trivial language (e.g. give us an awk string and we'll convert it to json and store it)

With this, we can tell you:
- What the three jobs that were deployed to a K8s cluster before this job started crashlooping
- ...
