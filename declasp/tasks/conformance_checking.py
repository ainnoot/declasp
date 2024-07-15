from collections import defaultdict
from dataclasses import dataclass

from declasp import Trace
from declasp.tasks.encoding_paths import DECLARE_ENCODING, CONFORMANCE_CHECKING_ENCODING
from typing import Dict

import clingo  # type: ignore

from declasp.log import StringEventLog
from declasp.declare import Model, Constraint
from declasp.utils import add_facts_to_backend
from itertools import chain


class CaptureModel:
    def __init__(self):
        self.by_trace = defaultdict(dict)
        self.by_constraint = defaultdict(dict)
        self.support = defaultdict(lambda: 0)

    def __call__(self, model: clingo.Model):
        for symbol in model.symbols(shown=True):
            tid = symbol.arguments[1].string
            cid = Constraint.from_id(symbol.arguments[0].number)
            self.by_trace[tid][cid] = symbol.name == "compliant"
            self.by_constraint[cid][tid] = symbol.name == "compliant"
            self.support[cid] += (1 if symbol.name == 'compliant' else 0)


@dataclass(frozen=True)
class ConformanceCheckingResult:
    by_trace: Dict[str, Dict[Constraint, bool]]
    by_constraint: Dict[Constraint, Dict[str, bool]]
    support: Dict[Constraint, float]

    def check_trace(self, trace_identifier: str):
        return self.by_trace[trace_identifier]

    def check_constraint(self, constraint: Constraint):
        return self.by_constraint[constraint]

    def as_json(self):
        data = dict()
        data['model'] = dict()
        data['result'] = dict()

        for con in self.by_constraint:
            con_json = con.as_json()
            con_json['support'] = round(self.support[con], 3)
            data['model'][str(con.id)] = con_json

        for trace, results in self.by_trace.items():
            data['result'][trace] = {c.id: value for c, value in results.items()}
        return data

def conformance_checking(model: Model, log: StringEventLog):
    if model.has_variables:
        raise Exception("Conformance checking requires a model without variables!")

    ctl = clingo.Control()
    ctl.load(CONFORMANCE_CHECKING_ENCODING.as_posix())
    ctl.load(DECLARE_ENCODING.as_posix())

    with ctl.backend() as backend:
        add_facts_to_backend(backend, chain(model.reify(), log.reify()))
    ctl.ground([("base", [])])
    model_trap = CaptureModel()
    _ = ctl.solve(on_model=model_trap)

    sz = log.number_of_traces()
    return ConformanceCheckingResult(model_trap.by_trace, model_trap.by_constraint, {c: s/sz for c, s in model_trap.support.items()})

def conformance_checking_single_trace(model: Model, t: Trace):
    if model.has_variables:
        raise Exception("Conformance checking requires a model without variables!")

    ctl = clingo.Control()
    ctl.load(CONFORMANCE_CHECKING_ENCODING.as_posix())
    ctl.load(DECLARE_ENCODING.as_posix())

    with ctl.backend() as backend:
        add_facts_to_backend(backend, chain(model.reify(), t.reify()))

        # a single trace is its own variant
        add_facts_to_backend(backend, [clingo.Function('case_identifier', [
            clingo.String(t.case_identifier), clingo.String(t.case_identifier)
        ])])
    ctl.ground([("base", [])])
    model_trap = CaptureModel()
    _ = ctl.solve(on_model=model_trap)

    return model_trap.by_trace[t.case_identifier]
