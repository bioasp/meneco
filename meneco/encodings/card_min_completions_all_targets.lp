% inputs from the met_net
% draft(Network).
% reaction(Reaction,Network).
% reversible(Reaction,Network).
% reactant(Species,Reaction).
% product(Species,Reaction).
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
% ireactions reactions are now defined in ireactions.lp


% repair
% choose interesting reactions to extend the network.
% dont extend with already existing reactions.

  { xreaction(R,N) : ireaction(R,N) }.


% operable reactions
% no xreaction if not all reactants in xscope

  oreaction(R,N) :- reaction(R,N), not draft(N), xscope(M) : reactant(M,R,N).
  oreaction(R,N) :- reaction(R,N), reversible(R,N), not draft(N), xscope(M) : product(M,R,N).

  :- xreaction(R,N), not oreaction(R,N).


% what is producible with the extensions

  xscope(M) :- seed(M).

  xscope(M) :- product(M,R,N), reaction(R,N), draft(N),
               xscope(M2) : reactant(M2,R,N).

  xscope(M) :- reactant(M,R,N), reaction(R,N), draft(N), reversible(R,N),
               xscope(M2) : product(M2,R,N).

  xscope(M) :- product(M,R,N), xreaction(R,N),
               xscope(M2) : reactant(M2,R,N).

  xscope(M) :- reactant(M,R,N), xreaction(R,N), reversible(R,N),
               xscope(M2) : product(M2,R,N).
               
% prohibit xreactions that produce nothing used by an operable reaction

  opreaction(R,N) :- reaction(R,N), xscope(M) : reactant(M,R,N).
  opreaction(R,N) :- reaction(R,N),reversible(R,N), xscope(M) : product(M,R,N).

  used(M) :- opreaction(R,N), reactant(M,R,N).
  used(M) :- opreaction(R,N), reversible(R,N), product(M,R,N).
  used(M) :- target(M).
  :- xreaction(R,N), not reversible(R,N), not used(M) : product(M,R,N).
  

% only one reaction for the same set of products 

%  sameprods(R1,R2) :- ireaction(R1,N), ireaction(R2,N2), R1<R2,
%                      product(M,R2,N2): product(M,R1,N).

%  :- xreaction(R1,N), xreaction(R2,M), sameprods(R1,R2).


% only one direction for reverse reactions

%  reverse(R1,R2) :- ireaction(R1,N), ireaction(R2,N2), R1<R2,
%                    reactant(M,R1,N): product(M,R2,N2),
%                    reactant(M,R2,N2): product(M,R1,N),
%                    product(M,R1,N): reactant(M,R2,N2),
%                    product(M,R2,N2): reactant(M,R1,N).

%  :- xreaction(R1,N), xreaction(R2,M), reverse(R1,R2).


% every xreaction must produce atleast one product that no other xreaction produces

%nunique(R,M) :- xreaction(R,N), product(M,R,N),
%                product(M,R2,N2),xreaction(R2,N2),R2!=R.
%:- xreaction(R,N), nunique(R,M) : product(M,R,N).

  
% every target that is potentially producible must be producible with the extension

  :- target(M), pscope(M), not xscope(M).


% optimizations

#minimize { 1@1, R,N : xreaction(R,N) ; 0@1}.

#show xreaction/2.
