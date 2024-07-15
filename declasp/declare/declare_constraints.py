import declasp.declare.constraint as C
import dataclasses

@dataclasses.dataclass(frozen=True, init=False)
class Choice(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Choice", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class ExclusiveChoice(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Exclusive Choice", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class Response(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Response", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class Precedence(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Precedence", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class Succession(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Succession", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class AlternateResponse(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Alternate Response", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class AlternatePrecedence(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Alternate Precedence", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class AlternateSuccession(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Alternate Succession", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class ChainResponse(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Chain Response", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class ChainPrecedence(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Chain Precedence", (a, b))


@dataclasses.dataclass(frozen=True, init=False)
class ChainSuccession(C.Constraint):
    def __init__(self, a, b):
        super().__init__("Chain Succession", (a, b))
