from declasp import Activity, Model
from declasp import Declare
from declasp import StringEventLog
from declasp.tasks import conformance_checking

if __name__ == "__main__":
    A, B, C, D = Activity.from_string("ER Triage,IV Liquid,CRP,Release A")
    X, Y = Activity.from_string("ER Triage,ER Sepsis Triage")
    model = Model()

    model.add_constraint(Declare.ChainResponse(A, B))
    model.add_constraint(Declare.Precedence(B, C))
    model.add_constraint(Declare.Choice(X, Y))
    log = StringEventLog.from_xes("tests/logs/sepsis.xes")

    result = conformance_checking(model, log)

    trace_id = "AA"
    constraint = Declare.Choice(X, Y)

    print(
        "Trace {} is compliant with {}? {}".format(
            trace_id, constraint, result.check_trace(trace_id)[constraint]
        )
    )
