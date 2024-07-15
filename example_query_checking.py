from declasp import Model
from declasp import Activity, ActivityVariable
from declasp import Declare
from declasp import StringEventLog
from declasp.tasks import query_checking

if __name__ == "__main__":
    A, B, C, D = Activity.from_string("a,b,c,d")
    X = ActivityVariable("x", (A, B))
    Y = ActivityVariable("y", (C, D))

    model = Model()
    model.add_constraint(Declare.ChainResponse(X, B))
    model.add_constraint(Declare.ChainResponse(B, Y))

    log = StringEventLog.from_strings([
        (1, ('a', 'b', 'd'), ('001', '003', '004')),
        (2, ('a', 'b', 'c'), ('002', '005'))
    ])

    results = query_checking(model, log, 0.1, 8)

    for i, result in enumerate(results):
        print(f"Answer #{i}")
        for var, val in result.assignment.items():
            print(var, val)

        print(result.support)
