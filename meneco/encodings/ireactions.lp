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
  dscope(M) :- seed(M).

  dscope(M) :- product(M,R,N), reaction(R,N), draft(N),
               dscope(M2) : reactant(M2,R,N).

  dscope(M) :- reactant(M,R,N), reaction(R,N), draft(N), reversible(R,N),
               dscope(M2) : product(M2,R,N).

% what is producible with all reactions

  pscope(M) :- seed(M).

  pscope(M) :- product(M,R,N), reaction(R,N),
               pscope(M2) : reactant(M2,R,N).

  pscope(M) :- reactant(M,R,N), reaction(R,N), reversible(R,N),
               pscope(M2) : product(M2,R,N).

% what are the interesting reactions

  bwd_interesting(M) :- target(M), not dscope(M), pscope(M).

  bwd_interesting(M) :- reactant(M,R,N), not dscope(M), bwd_reaction(R,N).

  bwd_interesting(M) :- product(M,R,N), not dscope(M), bwd_reaction(R,N), reversible(R,N).

  bwd_reaction(R,N) :- bwd_interesting(M), product(M,R,N), reaction(R,N).
  bwd_reaction(R,N) :- bwd_interesting(M), reactant(M,R,N), reaction(R,N), reversible(R,N).


  fwd_interesting(M) :- dscope(M).

  fwd_interesting(M) :- product(M,R,N),  fwd_reaction(R,N).
  fwd_interesting(M) :- reactant(M,R,N), fwd_reaction(R,N), reversible(R,N).

  fwd_reaction(R,N) :- fwd_interesting(M), reactant(M,R,N), product(M2,R,N), not dscope(M2), reaction(R,N).
  fwd_reaction(R,N) :- fwd_interesting(M), product(M,R,N), reactant(M2,R,N), not dscope(M2), reaction(R,N), reversible(R,N).

  % take care of reactions that produce something from nothing
  has_reactant(R) :- reactant(M,R,N).
  has_product(R)  :- product(M,R,N).
  fwd_reaction(R,N) :- product(M,R,N), not has_reactant(R), not dscope(M), reaction(R,N).
  fwd_reaction(R,N) :- reactant(M,R,N), not has_product(R), not dscope(M), reaction(R,N), reversible(R,N).


 ireaction(R,N) :- bwd_reaction(R,N), fwd_reaction(R,N).

#show ireaction/2.
