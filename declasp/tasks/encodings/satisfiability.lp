symbol(A) :- bind(_,_,A).
symbol("*").

#const a=0.
#const b=0.
{ last_timepoint(X): X=a..b-1 } = 1.
time(0..T) :- last_timepoint(T).

{ trace(0,T,A): symbol(A) } = 1 :- time(T).
:- last_timepoint(T), trace(0,T',_), T' > T.

:- constraint(C,_), fail(C,0).

#show.
#show trace(T,A): trace(0,T,A).