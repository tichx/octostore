from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.trace import Tracer
from opentelemetry.trace import Span

class Run:
    _current_run = None
    _name = None
    _current_span = None

    def __init__(self, run_name: str):
        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(ConsoleSpanExporter())
        )
        self._current_run = trace.get_tracer(run_name)
        self._name = run_name

    def start_run(self):
        self._current_run.start_as_current_span(self._name)
        self._current_span = self._current_run.CURRENT_SPAN
        return self._current_run

    def start_span(self, span_name: str):
        self._current_span = self.get_current_run().start_as_current_span(span_name)
        return self.get_current_span()

    def get_current_run(self) -> Tracer:
        return self._current_run

    def get_current_span(self) -> Span: 
        return self._current_span
