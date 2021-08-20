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

def extract_xreactions(model, return_atom=True) :
    lst = set(a[0] for pred in model if pred == 'xreaction' for a in model[pred])
    if return_atom : 
        atom = TermSet(Atom('xreaction(\"' +a[0]+'\",\"'+a[1]+'\")') for pred in model if pred == 'xreaction' for a in model[pred])
        return lst, atom
    else :
        return lst

def extract_unprod_traget(model) :
    return set(a[0] for pred in model if pred == 'unproducible_target' for a in model[pred])

def run_meneco(draft_sbml, seeds_sbml, targets_sbml, repair_sbml, enumeration = False):
    """Complete metabolic network by selecting reactions from a database

    Args:
        draft_sbml (str): SBML file name of metabolic network
        seeds_sbml (str): SBML file name seeds
        targets_sbml (str): SBML file name of targets
        repair_sbml (str): SBML file name of repair database
        enumeration (Boolean): enumeration boolean
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

    if repair_sbml:
        logger.info('\nReading repair network from ' + repair_sbml)
        repairnet = sbml.readSBMLnetwork(repair_sbml, 'repairnet')
        # repairnet.to_file("repairnet.lp")
        sys.stdout.flush()
        logger.info('done')
    else:
        repairnet = None
    results = run_meneco_from_asp(draftnet, seeds, targets, repairnet, enumeration)
    return results


def run_meneco_from_asp(draftnet, seeds, targets, repairnet, enumeration = False):
    """Performs all gap-filling steps from preprocessed data in ASP atom format. 

    Args:
        draftnet (TermSet): metabolic network atoms
        seeds (TermSet): seed atoms
        targets (TermSet): target atoms
        repairnet (TermSet): repair DB atoms
        enumeration (Boolean): enumeration boolean
    """
    # create results variables
    reconstructable_targets = set()
    essential_reactions_target = {}
    one_min_sol_lst = []
    intersection_sol_lst = []
    union_sol_lst = []
    enumeration_sol_lst = []
    results = {"unproducible_targets":None, "reconstructable_targets":None, "essential_reactions_by_target":None, "one_min_solution":None, "intersection_of_solutions":None, "union_of_solutions":None, "enumeration_of_solutions":None}

    # check producible targets and stop there if there are none

    logger.info('\nChecking draftnet for unproducible targets')
    model = query.get_unproducible(draftnet, targets, seeds)
    sys.stdout.flush()

    unproducible_targets_lst = extract_unprod_traget(model)
    logger.info(str(len(unproducible_targets_lst))+' unproducible targets:')
    logger.info("\n".join(unproducible_targets_lst))

    results["unproducible_targets"] = unproducible_targets_lst

    if repairnet == None:
        return unproducible_targets_lst, reconstructable_targets, essential_reactions_target, one_min_sol_lst, intersection_sol_lst, union_sol_lst, enumeration_sol_lst
    else:
        # check whether some targets can be reconstructed by gap-filling
        all_reactions = draftnet
        all_reactions = TermSet(all_reactions.union(repairnet))
        logger.info('\nChecking draftnet + repairnet for unproducible targets')
        model = query.get_unproducible(all_reactions, seeds, targets)
        print(model)
        unproducible_targets = extract_unprod_traget(model)

        logger.info('  still ' + str(len(unproducible_targets)) + ' unproducible targets:')
        logger.info("\n".join(unproducible_targets))
        never_producible = extract_unprod_traget(model)

        reconstructable_targets_atoms = TermSet()
        for t in unproducible_targets_lst:
            if not (t in never_producible):
                reconstructable_targets.add(t)
                reconstructable_targets_atoms.add(Atom('target(\"' +t+ '\")'))

        logger.info('\n ' + str(len(reconstructable_targets)) +
                    ' targets to reconstruct:')
        logger.info("\n".join(reconstructable_targets))

        results["reconstructable_targets"] = reconstructable_targets

        if len(reconstructable_targets) == 0:
            utils.clean_up()
            return results
        # perform gap-filling if there are reconstructable targets 
        else:
            essential_reactions = TermSet()
            essential_reactions_to_print = set()
            for t in reconstructable_targets:
                single_target = TermSet()
                single_target.add(Atom('target(\"' +t+ '\")'))
                logger.info('\nComputing essential reactions for ' + t)
                essentials = query.get_intersection_of_completions(
                    draftnet, repairnet, seeds, single_target)

                essentials_to_print, essentials_atoms = extract_xreactions(essentials, True)

                essential_reactions_target[t] = essentials_to_print
                
                logger.info(' ' + str(len(essentials_to_print)) + ' essential reactions found:')
                logger.info("\n".join(essentials_to_print))
                essential_reactions = TermSet(essential_reactions.union(essentials_atoms))
                essential_reactions_to_print = set(essential_reactions_to_print.union(essentials_to_print))
            
            logger.info('\nOverall ' + str(len(essential_reactions_to_print)) +
                        ' essential reactions found.')
            logger.info("\n".join(essential_reactions_to_print))

            results["essential_reactions_by_target"] = essential_reactions_target
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

            one_min_sol_lst = extract_xreactions(one_min_sol, False)
            optimum = len(one_min_sol_lst)
            logger.info("\n".join(one_min_sol_lst))

            results["one_min_solution"] = one_min_sol_lst

            logger.info('\nComputing common reactions in all completion with size ' +
                        str(optimum))
            intersection_sol = query.get_intersection_of_optimal_completions(
                draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum)

            intersection_sol_lst = extract_xreactions(intersection_sol, False)
            logger.info("\n".join(intersection_sol_lst))

            results["intersection_of_solutions"] = intersection_sol_lst

            logger.info('\nComputing union of reactions from all completion with size ' +
                        str(optimum))
            union_sol = query.get_union_of_optimal_completions(
                draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum)

            union_sol_lst = extract_xreactions(union_sol, False)
            logger.info("\n".join(union_sol_lst))

            results["union_of_solutions"] = union_sol_lst

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
                    model_lst = extract_xreactions(model, False)
                    enumeration_sol_lst.append(model_lst)
                    logger.info("\n".join(model_lst))
                #TODO provide clean lists, not list version of terms in what is returned
            else:
                enumeration_sol_lst = [] 
            results["enumeration_of_solutions"] = enumeration_sol_lst
            return results

if __name__ == '__main__':
    cmd_meneco(sys.argv[1:])
