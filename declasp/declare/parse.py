from declasp.declare.declare_constraints import (
    Choice,
    ExclusiveChoice,
    Response,
    AlternateResponse,
    ChainResponse,
    Precedence,
    AlternatePrecedence,
    ChainPrecedence,
    Succession,
    AlternateSuccession,
    ChainSuccession,
)

from declasp.declare.constraint import Activity
from declasp.declare.model import Model

__KNOWN_DECLARE_CONSTRAINTS__ = {
    "Choice": Choice,
    "Exclusive Choice": ExclusiveChoice,
    "Response": Response,
    "Precedence": Precedence,
    "Succession": Succession,
    "Alternate Response": AlternateResponse,
    "Alternate Precedence": AlternatePrecedence,
    "Alternate Succession": AlternateSuccession,
    "Chain Response": ChainResponse,
    "Chain Precedence": ChainPrecedence,
    "Chain Succession": ChainSuccession,
}


def declare_constraint_from_json(json_constraint):
    template = json_constraint["template"]
    arguments = json_constraint["arguments"]

    if template not in __KNOWN_DECLARE_CONSTRAINTS__:
        raise RuntimeError("Unknown Declare template:", template)

    arity = len(arguments)
    if arity != 2:
        raise RuntimeError(
            "Wrong arity for template", template, "expected 2 got", len(arguments)
        )

    params = [Activity(x) for x in arguments]
    return __KNOWN_DECLARE_CONSTRAINTS__[template](*params)


def declare_model_from_json(json_model):
    model = Model()
    for json_constraint in json_model:
        model.add_constraint(declare_constraint_from_json(json_constraint))
    return model
