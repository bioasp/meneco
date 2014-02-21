% inputs from the met_net
% species(Species).
% reaction(Reaction,Network).
% reactant(Species,Reaction).
% product(Species,Reaction).
% draft(Network).
% seed(Species).
% target(Species).

% find minimal set of xreactions such that xscope contains targets in pscope

% what is producible by the original network

  dreaction(R) :- reaction(R,N), draft(N).

  dscope(M) :- seed(M).

  dscope(M) :- product(M,R,N), reaction(R,N), draft(N),
               dscope(M2) : reactant(M2,R,N).

  dscope(M) :- reactant(M,R,N), reaction(R,N), draft(N), reversible(R),
               dscope(M2) : product(M2,R,N).

% what is producible with all reactions

  pscope(M) :- seed(M).

  pscope(M) :- product(M,R,N), reaction(R,N),
               pscope(M2) : reactant(M2,R,N).

  pscope(M) :- reactant(M,R,N), reaction(R,N), reversible(R),
               pscope(M2) : product(M2,R,N).

% what are the interesting reactions

  interesting(M) :- target(M), not dscope(M), pscope(M).

  interesting(M) :- reactant(M,R,N), not dscope(M), iireaction(R,N).

  interesting(M) :- product(M,R,N), not dscope(M), iireaction(R,N), reversible(R).

  iireaction(R,N) :- interesting(M), product(M,R,N), reaction(R,N).
  iireaction(R,N) :- interesting(M), reactant(M,R,N), reaction(R,N), reversible(R).


  binteresting(M) :- dscope(M).

  binteresting(M) :- product(M,R,N), bireaction(R,N).
  binteresting(M) :- reactant(M,R,N), bireaction(R,N), reversible(R).

  bireaction(R,N) :- binteresting(M), reactant(M,R,N), product(M2,R,N), not dscope(M2), reaction(R,N).
  bireaction(R,N) :- binteresting(M), product(M,R,N), reactant(M2,R,N), not dscope(M2), reaction(R,N), reversible(R).

 ireaction(R,N) :- iireaction(R,N), bireaction(R,N), not dreaction(R).
%  ireaction(R,N) :- iireaction(R,N), bireaction(R,N), not draft(N).

%  iscope(M) :- seed(M).

%  iscope(M) :- product(M,R,N), reaction(R,N), draft(N),
%               iscope(M2) : reactant(M2,R,N).

%  iscope(M) :- reactant(M,R,N), reaction(R,N), draft(N), reversible(R),
%               iscope(M2) : product(M2,R,N).

%  iscope(M) :- product(M,R,N), ireaction(R,N),
%               iscope(M2) : reactant(M2,R,N).

%  iscope(M) :- reactant(M,R,N), ireaction(R,N), reversible(R),
%               iscope(M2) : product(M2,R,N).

%:- target(X), pscope(X), not iscope(X).

#hide.
#show ireaction/2.

