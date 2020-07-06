from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.trace import Tracer
from opentelemetry.trace import Span

import datetime
from pathlib import Path


class Run:
    _current_run = None
    _name = None
    _current_span = None

    def __init__(self, run_name: str):
        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )
        run_name = (
            run_name or f"{Path(__file__).parent}-{datetime.datetime.now().microsecond}"
        )
        self._current_run = trace.get_tracer(run_name or run_name)
        self._name = run_name

    def start_run(self, start_time=None, tags=None):
        self._current_run.start_as_current_span(self._name)
        self._current_span = self._current_run.CURRENT_SPAN
        self._current_span.set_attribute(
            "start_time", start_time or datetime.datetime.now().isoformat
        )
        self._current_span.set_attribute("tags", tags)
        return self._current_run

    def start_span(self, span_name: str):
        self._current_span = self.get_current_run().start_as_current_span(span_name)
        return self.get_current_span()

    def get_current_run(self) -> Tracer:
        return self._current_run

    def get_current_span(self) -> Span:
        return self._current_span
