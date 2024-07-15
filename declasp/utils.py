from typing import Iterable, Tuple, Dict, List
from collections import defaultdict
import polars as pl  # type: ignore
import clingo  # type: ignore
import rustxes  # type: ignore


def integer_sequence():
    x = 0
    while True:
        yield x
        x += 1


def add_fact_to_backend(backend: clingo.Backend, symbol: clingo.Symbol):
    lit = backend.add_atom(symbol)
    backend.add_rule([lit], [])
    return lit


def add_facts_to_backend(backend: clingo.Backend, symbols: Iterable[clingo.Symbol]):
    for symbol in symbols:
        add_fact_to_backend(backend, symbol)


def get_variants(events: pl.DataFrame):
    events_by_case_id = events.groupby("case:concept:name")

    variants: Dict[Tuple[str, ...], List[str]] = defaultdict(list)

    for tid, trace_events in events_by_case_id:
        trace = trace_events.sort("time:timestamp", maintain_order=True)
        activities = tuple(trace["concept:name"])
        variants[activities].append(str(tid))

    return {
        vid: (activities, trace_ids)
        for vid, (activities, trace_ids) in enumerate(variants.items())
    }


def import_xes_log(log_path: str):
    data, _ = rustxes.import_xes(log_path)
    return data
