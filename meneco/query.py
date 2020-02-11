# Copyright (c) 2014, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of meneco.
#
# meneco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# meneco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with meneco.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
import os
from pyasp.term import *
from pyasp.asp import *


root                      = __file__.rsplit('/', 1)[0]
unproducible_prg          = root + '/encodings/unproducible_targets.lp'
ireaction_prg             = root + '/encodings/ireactions.lp'
minimal_completion_prg    = root + '/encodings/card_min_completions_all_targets.lp'
heuristic_prg             = root + '/encodings/heuristic.lp'
minimal_completion_wb_prg = root + '/encodings/card_min_completions_all_targets_with_bounds.lp'
completion_prg            = root + '/encodings/completions_all_targets.lp'


def get_mapping_ireaction(termset):
    dict    = {}
    revdict = {}
    for a in termset:
      if a.pred() == "ireaction" :
        if not a.arg(0) in dict:
          id             = len(dict)
          dict[a.arg(0)] = id
          revdict[id]    = a.arg(0)
    return dict, revdict


def map_reaction_ids(termset, dict):
    mapped = TermSet()
    for a in termset:
      if a.pred() == "reaction" :
        if a.arg(0) in dict:
          mapped.add(Term('reaction', [str(dict[a.arg(0)]), a.arg(1)]))
        else : mapped.add(a)

      elif a.pred() == "xreaction" :
        if a.arg(0) in dict:
          mapped.add(Term('xreaction', [str(dict[a.arg(0)]), a.arg(1)]))
        else : mapped.add(a)

      elif a.pred() == "ireaction" :
        if a.arg(0) in dict:
          mapped.add(Term('ireaction', [str(dict[a.arg(0)]), a.arg(1)]))
        else : print("Error: unknown ireaction, query.py line 64")

      elif a.pred() == "value" :
        if a.arg(0) in dict:
          mapped.add(Term('value', [str(dict[a.arg(0)]), a.arg(1)]))
        else : mapped.add(a)

      elif a.pred() == "product" :
        if a.arg(1) in dict:
          mapped.add(Term('product', [a.arg(0), str(dict[a.arg(1)]),a.arg(2)]))
        else : mapped.add(a)

      elif a.pred() == "reactant" :
        if a.arg(1) in dict:
          mapped.add(Term('reactant', [a.arg(0), str(dict[a.arg(1)]),a.arg(2)]))
        else : mapped.add(a)

      elif a.pred() == "reversible" :
        if a.arg(0) in dict:
          mapped.add(Term('reversible', [str(dict[a.arg(0)])]))
        else : mapped.add(a)
      else :
        mapped.add(a)

    return mapped


def unmap_reaction_ids(termset, revdict):
    unmapped = TermSet()
    for a in termset:
      if a.pred() == "xreaction" :
        unmapped.add(Term('xreaction', [str(revdict[int(a.arg(0))]), a.arg(1)]))

    return unmapped


def get_unproducible(draft, seeds, targets):
    draft_f  = draft.to_file()
    seed_f   =  seeds.to_file()
    target_f = targets.to_file()
    prg      = [unproducible_prg, draft_f, seed_f, target_f ]
    solver   = Gringo4Clasp()
    models   = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return models[0]


def compute_ireactions(instance):
    instance_f = instance.to_file()
    prg        = [ ireaction_prg, instance_f]
    solver     = Gringo4Clasp()
    models     = solver.run(prg,collapseTerms=True, collapseAtoms=False)
    os.unlink(instance_f)
    assert(len(models) == 1)
    return models[0]


def get_minimal_completion_size(draft, repairnet, seeds, targets):

    draftfact  = String2TermSet('draft("draft")')
    instance   = TermSet(draft.union(draftfact).union(repairnet).union(targets).union(seeds))
    ireactions = compute_ireactions(instance)
    instance   = TermSet(instance.union(ireactions))
    instance_f = instance.to_file()

    prg        = [minimal_completion_prg, instance_f]

    co         = "--configuration=jumpy --opt-strategy=5"
    solver     = Gringo4Clasp(clasp_options=co)

    optimum    = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(instance_f)
    return optimum


def get_intersection_of_optimal_completions(draft, repairnet, seeds, targets, optimum):

    draftfact  = String2TermSet('draft("draft")')
    instance   = TermSet(draft.union(draftfact).union(repairnet).union(targets).union(seeds))
    ireactions = compute_ireactions(instance)
    instance   = TermSet(instance.union(ireactions))
    instance_f = instance.to_file()

    prg        = [minimal_completion_prg, instance_f]

    options    = '--configuration jumpy --opt-strategy=5 --enum-mode cautious --opt-mode=optN --opt-bound='+str(optimum)

    solver     = Gringo4Clasp(clasp_options=options)

    intersec   = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(instance_f)
    return intersec[0]


def get_union_of_optimal_completions(draft, repairnet, seeds, targets, optimum):

    draftfact  = String2TermSet('draft("draft")')
    instance   = TermSet(draft.union(draftfact).union(repairnet).union(targets).union(seeds))
    ireactions = compute_ireactions(instance)
    instance   = TermSet(instance.union(ireactions))
    instance_f = instance.to_file()

    prg        = [minimal_completion_prg, instance_f]

    options    = '--configuration jumpy --opt-strategy=5 --enum-mode brave --opt-mode=optN --opt-bound='+str(optimum)

    solver     = Gringo4Clasp(clasp_options=options)

    union      = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(instance_f)
    return union[0]


def get_optimal_completions(draft, repairnet, seeds, targets, optimum, nmodels=0):

    draftfact  = String2TermSet('draft("draft")')
    instance   = TermSet(draft.union(draftfact).union(repairnet).union(targets).union(seeds))
    ireactions = compute_ireactions(instance)
    instance   = TermSet(instance.union(ireactions))
    instance_f = instance.to_file()

    prg        = [minimal_completion_prg, instance_f]

    options    = str(nmodels)+' --configuration jumpy --opt-strategy=5 --opt-mode=optN --opt-bound='+str(optimum)
    solver     = Gringo4Clasp(clasp_options=options)
    models     = solver.run(prg, collapseTerms=True, collapseAtoms=False)

    os.unlink(instance_f)
    return models


def get_intersection_of_completions(draft, repairnet, seeds, targets):

    draftfact  = String2TermSet('draft("draft")')
    instance   = TermSet(draft.union(draftfact).union(repairnet).union(targets).union(seeds))
    ireactions = compute_ireactions(instance)
    instance   = TermSet(instance.union(ireactions))
    instance_f = instance.to_file()

    prg        = [completion_prg, instance_f]
    options    = '--enum-mode cautious --opt-mode=ignore '

    solver     = Gringo4Clasp(clasp_options=options)
    models     = solver.run(prg, collapseTerms=True, collapseAtoms=False)
    os.unlink(instance_f)
    return models[0]
