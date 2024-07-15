from dataclasses import dataclass
from typing import Dict, List

from declasp.declare import Model
from declasp.log import StringEventLog
import clingo  # type: ignore
from declasp.tasks.encoding_paths import DECLARE_ENCODING, QUERY_CHECKING_ENCODING
from declasp.utils import add_facts_to_backend, add_fact_to_backend
from itertools import chain

from math import ceil

class CaptureModels:
    def __init__(self, log_length):
        self.results = []
        self.log_length = log_length

    def __call__(self, model: clingo.Model):
        assignment = dict()
        support = 0.0
        for symbol in model.symbols(shown=True):
            if symbol.name == "support":
                support = symbol.arguments[0].number / self.log_length
                continue

            var = symbol.arguments[0].string
            val = symbol.arguments[1].string
            assignment[var] = val

        self.results.append(QueryCheckingResult(assignment, support))

@dataclass(frozen=True)
class QueryCheckingResult:
    assignment: Dict[str, str]
    support: float


def query_checking(model: Model, log: StringEventLog, min_support: float, k: int) -> List[QueryCheckingResult]:
    """
    Returns up to `k` solutions to the query checking problem.
    """

    if not model.has_variables:
        raise Exception("Query checking requires a model with at least one variable!")

    ctl = clingo.Control()
    ctl.configuration.solve.models = k
    ctl.load(QUERY_CHECKING_ENCODING.as_posix())
    ctl.load(DECLARE_ENCODING.as_posix())

    log_length = log.number_of_traces()
    inf = ceil(min_support * log_length)

    with ctl.backend() as backend:
        add_facts_to_backend(backend, chain(model.reify(), log.reify()))
        for var in model.variables:
            add_facts_to_backend(backend, var.reify())

        add_fact_to_backend(backend, clingo.Function("min_supp", [clingo.Number(inf)]))

    ctl.ground([("base", [])])

    model_trap = CaptureModels(log_length)
    _ = ctl.solve(on_model=model_trap)

    return model_trap.results
