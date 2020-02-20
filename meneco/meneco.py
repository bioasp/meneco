#!python
# Copyright (c) 2012, Sven Thiele <sthiele78@gmail.com>
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
import argparse
import sys
from meneco import utils, sbml, query
import logging
import clyngor
from clyngor import as_pyasp
from clyngor.as_pyasp import TermSet, Atom

logger = logging.getLogger(__name__)


def cmd_meneco(argv):
    """Run meneco from shell
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--draftnet",
                        help='metabolic network in SBML format', required=True)
    parser.add_argument("-s", "--seeds",
                        help='seeds in SBML format', required=True)
    parser.add_argument("-t", "--targets",
                        help='targets in SBML format', required=True)

    parser.add_argument('-r', '--repairnet',
                        help='perform network completion using REPAIRNET '
                        'a metabolic network in SBML format')

    parser.add_argument('--enumerate',
                        help='enumerate all minimal completions',
                        action='store_true',
                        default=False)

    args = parser.parse_args(argv)
    draft_sbml = args.draftnet
    repair_sbml = args.repairnet
    seeds_sbml = args.seeds
    targets_sbml = args.targets

    run_meneco(draft_sbml, seeds_sbml, targets_sbml,
               repair_sbml, args.enumerate)

def extract_xreactions(model, return_atom=True, return_set = False) :
    if return_set :
        lst = set(a[0] for pred in model if pred == 'xreaction' for a in model[pred])
    else :
        lst = [a[0] for pred in model if pred == 'xreaction' for a in model[pred]]
    if return_atom : 
        atom = TermSet(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")') for pred in model if pred == 'xreaction' for a in model[pred])
        return lst, atom
    else :
        return lst

def run_meneco(draft_sbml, seeds_sbml, targets_sbml, repair_sbml, enumeration):
    """Complete metabolic network by selecting reactions from a database

    Args:
        draft_sbml (str): SBML file name of metabolic network
        seeds_sbml (str): SBML file name seeds
        targets_sbml (str): SBML file name of targets
        repair_sbml (str): SBML file name of repair database
    """
    logger.info('Reading draft network from ' + draft_sbml)
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft')
    # draftnet.to_file("draftnet.lp")

    logger.info('Reading seeds from ' + seeds_sbml)
    seeds = sbml.readSBMLseeds(seeds_sbml)
    # seeds.to_file("seeds.lp")

    logger.info('Reading targets from ' + targets_sbml)
    targets = sbml.readSBMLtargets(targets_sbml)
    # targets.to_file("targets.lp")

    logger.info('\nChecking draftnet for unproducible targets')
    model = query.get_unproducible(draftnet, targets, seeds)
    sys.stdout.flush()

    unproducible_targets_lst = []
    # unproducible_targets_atoms = TermSet()
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                # unproducible_targets_atoms.add(Atom('unproducible_target', ['"'+a[0]+'"']))
                unproducible_targets_lst.append(a[0])
    logger.info(str(len(unproducible_targets_lst))+' unproducible targets:')
    logger.info("\n".join(unproducible_targets_lst))

    if repair_sbml == None:
        return(unproducible_targets_lst)
    
    logger.info('\nReading repair network from ' + repair_sbml)
    repairnet = sbml.readSBMLnetwork(repair_sbml, 'repairnet')
    # repairnet.to_file("repairnet.lp")
    sys.stdout.flush()
    logger.info('done')

    all_reactions = draftnet
    all_reactions = TermSet(all_reactions.union(repairnet))
    logger.info('\nChecking draftnet + repairnet for unproducible targets')
    model = query.get_unproducible(all_reactions, seeds, targets)
    unproducible_targets = []
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                unproducible_targets.append(a[0])

    logger.info('  still ' + str(len(unproducible_targets)) + ' unproducible targets:')
    logger.info("\n".join(unproducible_targets))
    never_producible = []
    # never_productible_atoms = TermSet()
    for pred in model :
        if pred == 'unproducible_target':
            for a in model[pred, 1]:
                # never_productible_atoms.add(Atom('target', ['\"'+a[0]+'\"']))
                never_producible.append(a[0])

    reconstructable_targets = []
    reconstructable_targets_atoms = TermSet()
    for t in unproducible_targets_lst:
        if not (t in never_producible):
            reconstructable_targets.append(t)
            reconstructable_targets_atoms.add(Atom('target(\"' +t+ '\")'))

    logger.info('\n ' + str(len(reconstructable_targets)) +
                ' targets to reconstruct:')
    logger.info("\n".join(reconstructable_targets))

    if len(reconstructable_targets) == 0:
        utils.clean_up()
        quit()


    essential_reactions = TermSet()
    essential_reactions_to_print = set()
    essential_reactions_target = {}
    for t in reconstructable_targets:
        single_target = TermSet()
        single_target.add(Atom('target(\"' +t+ '\")'))
        logger.info('\nComputing essential reactions for ' + t)
        essentials = query.get_intersection_of_completions(
            draftnet, repairnet, seeds, single_target)
        
        # essentials_to_print = set()
        # essentials_atoms = TermSet()
        # for pred in essentials :
        #     if pred == 'xreaction':
        #         for a in essentials[pred]:
        #             essentials_atoms.add(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")'))
        #             essentials_to_print.add(a[0])
        
        essentials_to_print, essentials_atoms = extract_xreactions(essentials, True)

        essential_reactions_target[t] = essentials_to_print
        
        logger.info(' ' + str(len(essentials_to_print)) + ' essential reactions found:')
        logger.info("\n".join(essentials_to_print))
        essential_reactions = TermSet(essential_reactions.union(essentials_atoms))
        essential_reactions_to_print = set(essential_reactions_to_print.union(essentials_to_print))
    
    logger.info('\nOverall ' + str(len(essential_reactions_to_print)) +
                ' essential reactions found.')
    logger.info("\n".join(essential_reactions_to_print))


    logger.info('\nAdding essential reactions to network.')
    draftnet = TermSet(draftnet.union(essential_reactions))

    utils.clean_up()

    # draftnet.to_file("draft.lp")
    # repairnet.to_file("repairnet.lp")
    # unproducible_targets.to_file("targets.lp")
    # seeds.to_file("seeds.lp")


    logger.info('\nComputing one minimal completion to produce all targets')
    one_min_sol = query.get_minimal_completion_size(
        draftnet, repairnet, seeds, reconstructable_targets_atoms)

    # one_min_sol_lst = []
    # # min_sol_atoms = TermSet()
    # for pred in one_min_sol :
    #     if pred == 'xreaction':
    #         for a in one_min_sol[pred]:
    #             # min_sol_atoms.add(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")'))
    #             one_min_sol_lst.append(a[0])    

    one_min_sol_lst = extract_xreactions(one_min_sol, False)
    optimum = len(one_min_sol_lst)
    logger.info("\n".join(one_min_sol_lst))


    logger.info('\nComputing common reactions in all completion with size ' +
                str(optimum))
    intersection_sol = query.get_intersection_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum)
    # intersection_sol_lst = []
    # # intersection_sol_atom = TermSet()
    # for pred in intersection_sol :
    #     if pred == 'xreaction':
    #         for a in intersection_sol[pred]:
    #             intersection_sol_lst.append(a[0])
    #             # intersection_sol_atom.add(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")'))
    # 

    intersection_sol_lst = extract_xreactions(intersection_sol, False)
    logger.info("\n".join(intersection_sol_lst))

    logger.info('\nComputing union of reactions from all completion with size ' +
                str(optimum))
    union_sol = query.get_union_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum)
    # union_sol_lst = []
    # # union_sol_atom = TermSet()
    # for pred in union_sol :
    #     if pred == 'xreaction':
    #         for a in union_sol[pred]:
    #             union_sol_lst.append(a[0])
    #             # union_sol_atom.add(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")'))

    union_sol_lst = extract_xreactions(union_sol, False)
    logger.info("\n".join(union_sol_lst))

    if enumeration:
        logger.info('\nComputing all completions with size ' +
                    str(optimum))
        enumeration_sol = query.get_optimal_completions(
            draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum)
        count = 1
        enumeration_sol_lst = []
        for model in enumeration_sol:
            logger.info('Completion ' + str(count) + ': ')
            count += 1
            # model_lst = set()
            # # model_lst_atom = TermSet()
            # for pred in model :
            #     if pred == "xreaction":
            #         for a in model[pred]: 
            #             model_lst.add(a[0])
            #             # model_lst_atom.add(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")'))
            model_lst = extract_xreactions(model, False, True)
            enumeration_sol_lst.append(model_lst)
            logger.info("\n".join(model_lst))
        #TODO provide clean lists, not list version of terms in what is returned
    else:
        enumeration_sol_lst = [] 
    
    return unproducible_targets_lst, reconstructable_targets, essential_reactions_target, one_min_sol_lst, intersection_sol_lst, union_sol_lst, enumeration_sol_lst



if __name__ == '__main__':
    cmd_meneco(sys.argv[1:])
