from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, Generator, List
import clingo  # type: ignore
from declasp.utils import get_variants, import_xes_log


@dataclass(frozen=True)
class Trace:
    case_identifier: str
    events: Tuple[str, ...]

    def reify(self):
        for t, a in enumerate(self.events):
            yield clingo.Function(
                "trace",
                [
                    clingo.String(self.case_identifier),
                    clingo.Number(t),
                    clingo.String(a),
                ],
            )

    @staticmethod
    def from_csv(csv, identifier):
        quoted_events = csv.split(",")
        events = []
        for x in quoted_events:
            events.append(x)

        return Trace(identifier, csv)


@dataclass(frozen=True)
class StringEventLog:
    variants: Dict[int, Tuple[Tuple[str, ...], Tuple[str, ...]]]
    reverse_index: Dict[str, int]

    def number_of_traces(self):
        cnt = 0
        for var, (_, tids) in self.variants.items():
            cnt += len(tids)
        return cnt

    def __iter__(self):
        for vid, (events, tids) in self.variants.items():
            yield vid, events, tids

    def reify(self) -> Generator[clingo.Symbol, None, None]:
        for vid, (events, tids) in self.variants.items():
            yield clingo.Function(
                "weight", [clingo.Number(vid), clingo.Number(len(tids))]
            )

            for tid in tids:
                yield clingo.Function(
                    "case_identifier", [clingo.Number(vid), clingo.String(tid)]
                )

            for t, e in enumerate(events):
                yield clingo.Function(
                    "trace", [clingo.Number(vid), clingo.Number(t), clingo.String(e)]
                )

    @staticmethod
    def from_strings(inputs: List[Tuple[int, Tuple[str, ...], Tuple[str, ...]]]):
        reverse_index = dict()
        variants = dict()
        for vid, activities, tids in inputs:
            variants[vid] = (activities, tids)
            for tid in tids:
                reverse_index[tid] = vid
        return StringEventLog(variants, reverse_index)

    @staticmethod
    def from_xes(log_path: str):
        log = import_xes_log(log_path)
        variants = get_variants(log)
        reverse_index = dict()
        for vid, (trace, tids) in variants.items():
            for tid in tids:
                reverse_index[tid] = vid

        return StringEventLog(variants, reverse_index)

    def trace_by_case_identifier(self, case_identifier):
        vid = self.reverse_index[case_identifier]
        return Trace(case_identifier, self.variants[vid][0])
