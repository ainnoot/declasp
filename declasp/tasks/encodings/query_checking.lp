{ assign(Var, Val): domain(Var, Val) } = 1 :- var_bind(_, _, Var).

bind(C, Arg, Val) :- var_bind(C, Arg, Var), assign(Var, Val).
compliant(C,VID) :- not fail(C,VID), constraint(C,_), trace(VID,_,_).
support(S) :- S =#sum{F,VID: weight(VID,F), not fails(VID)}.
:- min_supp(X), support(S), S < X.
fails(VID) :- constraint(C,_), fail(C,VID).

#show.
#defined assign/2.
#defined support/1.
#show assign/2.
#show support/1.