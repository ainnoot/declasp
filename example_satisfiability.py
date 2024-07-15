from declasp import Model
from declasp import Activity
from declasp import Declare
from declasp.tasks import satisfiability

if __name__ == "__main__":
    A, B, C = Activity.from_string("IV Liquid,CRP,Release A")

    model = Model()
    model.add_constraint(Declare.ChainResponse(A, B))
    model.add_constraint(Declare.ChainResponse(B, C))
    model.add_constraint(Declare.Choice(A, B))

    res = satisfiability(model, 8)

    print(res)
