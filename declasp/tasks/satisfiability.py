import clingo  # type: ignore
from declasp.utils import add_facts_to_backend
from declasp.declare import Model
from declasp.tasks.encoding_paths import DECLARE_ENCODING, SATISFIABILITY_ENCODING


class CaptureModel:
    def __init__(self):
        self.trace = []

    def __call__(self, model: clingo.Model):
        for symbol in model.symbols(shown=True):
            time = symbol.arguments[0].number
            event = symbol.arguments[1].string
            self.trace.append((time, event))

    def as_tuple(self):
        trace = sorted(self.trace)
        return tuple(x[1] for x in trace)


def bound_satisfiability(model: Model, a, b):
    ctl = clingo.Control([f"-c a={a}", f"-c b={b}"])

    ctl.load(DECLARE_ENCODING.as_posix())
    ctl.load(SATISFIABILITY_ENCODING.as_posix())

    with ctl.backend() as backend:
        add_facts_to_backend(backend, model.reify())
    ctl.ground([("base", [])])

    trace_trap = CaptureModel()
    ans = ctl.solve(on_model=trace_trap)

    if ans.satisfiable:
        return trace_trap.as_tuple()
    return None


def satisfiability(model: Model, max_length):
    if model.has_variables:
        raise Exception("Satisfiability requires a model without variables!")

    a = 0
    b = 1
    ans = None

    while ans is None and b <= max_length:
        ans = bound_satisfiability(model, a, b)
        a, b = b, b * 2

    if ans is None:
        return {"found_model": False, "reached_horizon": a}
    else:
        return {"found_model": True, "reached_horizon": a, "witness": ans}
