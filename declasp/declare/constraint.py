from dataclasses import dataclass
from typing import Tuple, Generator, Union, Iterable, Dict
from declasp.utils import integer_sequence
import clingo  # type: ignore


class ConstraintsById:
    id_to_constraint: Dict[int, "Constraint"] = dict()
    constraint_to_id: Dict["Constraint", int] = dict()
    CONSTRAINT_ID_SEQUENCE = integer_sequence()

    @staticmethod
    def register(constraint: "Constraint"):
        if constraint in ConstraintsById.constraint_to_id:
            return

        fresh_id = next(ConstraintsById.CONSTRAINT_ID_SEQUENCE)
        ConstraintsById.constraint_to_id[constraint] = fresh_id
        ConstraintsById.id_to_constraint[fresh_id] = constraint


@dataclass(frozen=True)
class Activity:
    value: str

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(activity_string, sep=","):
        return tuple(Activity(x.strip()) for x in activity_string.split(sep))

    @staticmethod
    def from_iterable(it: Iterable[str]):
        return tuple(Activity(x.strip()) for x in it)

    def reify_name(self):
        return clingo.String(self.value)


@dataclass(frozen=True)
class ActivityVariable:
    value: str
    domain: Tuple[Activity, ...]

    def __str__(self):
        return "$" + self.value

    def reify(self) -> Generator[clingo.Symbol, None, None]:
        for possible_value in self.domain:
            yield clingo.Function(
                "domain", [clingo.String(self.value), possible_value.reify_name()]
            )

    def reify_name(self):
        return clingo.String(self.value)


@dataclass(frozen=True)
class Constraint:
    template: str
    arguments: Tuple[Union[Activity, ActivityVariable], ...]

    def __str__(self):
        return "{}({})".format(self.template, ",".join(str(x) for x in self.arguments))

    def as_json(self):
        return {"template": self.template, "arguments": [a.value for a in self.arguments]}

    def __post_init__(self):
        ConstraintsById.register(self)

    @property
    def id(self):
        return ConstraintsById.constraint_to_id[self]

    @staticmethod
    def from_id(x: int):
        return ConstraintsById.id_to_constraint[x]

    def reify(self):
        yield clingo.Function(
            "constraint", [clingo.Number(self.id), clingo.String(self.template)]
        )

        for arg_pos, arg in enumerate(self.arguments):
            if not isinstance(arg, ActivityVariable):
                yield clingo.Function(
                    "bind",
                    [
                        clingo.Number(self.id),
                        clingo.Function("arg_" + str(arg_pos), []),
                        arg.reify_name(),
                    ],
                )

            else:
                yield clingo.Function(
                    "var_bind",
                    [
                        clingo.Number(self.id),
                        clingo.Function("arg_" + str(arg_pos), []),
                        arg.reify_name(),
                    ],
                )
