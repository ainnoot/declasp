compliant(C,TID) :- not fail(C,VID), constraint(C,_), trace(VID,_,_), case_identifier(VID,TID).
failure(C,TID) :- fail(C,VID), case_identifier(VID,TID).

#defined compliant/2.
#defined failure/2.
#show.
#show compliant/2.
#show failure/2.