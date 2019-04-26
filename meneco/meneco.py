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
from pyasp.term import *
from pyasp.asp import *
from meneco import query, utils, sbml
import logging

logger = logging.getLogger(__name__)


def cmd_meneco():
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
                        default='False')

    args = parser.parse_args()
    draft_sbml = args.draftnet
    repair_sbml = args.repairnet
    seeds_sbml = args.seeds
    targets_sbml = args.targets

    run_meneco(draft_sbml, seeds_sbml, targets_sbml,
               repair_sbml, args.enumerate)


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
    print(' ', len(model), 'unproducible targets:')
    utils.print_met(model.to_list())
    unproducible_targets = TermSet()
    unprod_lst = []
    for a in model:
        target = str(a)[13:]
        t = String2TermSet(target)
        unprod_lst.append(target)
        unproducible_targets = TermSet(unproducible_targets.union(t))

    if repair_sbml == None:
        return(unprod_lst)

    logger.info('\nReading repair network from ' + repair_sbml)
    repairnet = sbml.readSBMLnetwork(repair_sbml, 'repairnet')
    # repairnet.to_file("repairnet.lp")

    all_reactions = draftnet
    all_reactions = TermSet(all_reactions.union(repairnet))
    logger.info('\nChecking draftnet + repairnet for unproducible targets')
    sys.stdout.flush()
    model = query.get_unproducible(all_reactions, seeds, targets)
    logger.info('  still ' + str(len(model)) + ' unproducible targets:')
    utils.print_met(model.to_list())
    never_producible = TermSet()
    for a in model:
        target = str(a)[13:]
        t = String2TermSet(target)
        never_producible = TermSet(never_producible.union(t))

    reconstructable_targets = TermSet()
    targets_to_reconstruct = []
    for t in unproducible_targets:
        if not (t in never_producible):
            reconstructable_targets.add(t)
            targets_to_reconstruct.append(str(t.arg(0)))
    logger.info('\n ' + str(len(reconstructable_targets)) +
                ' targets to reconstruct:')
    utils.print_met(reconstructable_targets)

    if len(reconstructable_targets) == 0:
        utils.clean_up()
        quit()

    essential_reactions = TermSet()
    for t in reconstructable_targets:
        single_target = TermSet()
        single_target.add(t)
        logger.info('\nComputing essential reactions for ' + t.arg(0))
        essentials = query.get_intersection_of_completions(
            draftnet, repairnet, seeds, single_target)
        logger.info(' ' + str(len(essentials)) + ' essential reactions found:')
        utils.print_met(essentials.to_list())
        essential_reactions = TermSet(essential_reactions.union(essentials))
    logger.info('\nOverall' + str(len(essential_reactions)) +
                ' essential reactions found.')
    utils.print_met(essential_reactions)
    logger.info('\nAdding essential reactions to network.')
    draftnet = TermSet(draftnet.union(essential_reactions))

    utils.clean_up()

    # draftnet.to_file("draft.lp")
    # repairnet.to_file("repairnet.lp")
    # unproducible_targets.to_file("targets.lp")
    # seeds.to_file("seeds.lp")

    logger.info('\nComputing one minimal completion to produce all targets')
    one_min_sol = query.get_minimal_completion_size(
        draftnet, repairnet, seeds, reconstructable_targets)
    optimum = one_min_sol[0].score[0]
    one_min_sol_lst = one_min_sol[0].to_list()
    utils.print_met(one_min_sol_lst)

    logger.info('\nComputing common reactions in all completion with size ' +
                str(optimum))
    intersection_sol = query.get_intersection_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets,  optimum)
    intersection_sol_lst = intersection_sol.to_list()
    utils.print_met(intersection_sol_lst)

    logger.info('\nComputing union of reactions from all completion with size ' +
                str(optimum))
    union_sol = query.get_union_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets, optimum)
    union_sol_lst = union_sol.to_list()
    utils.print_met(union_sol_lst)

    if enumeration:
        logger.info('\nComputing all completions with size ' +
                    str(optimum))
        sys.stdout.flush()
        enumeration_sol = query.get_optimal_completions(
            draftnet, repairnet, seeds, reconstructable_targets, optimum)
        count = 1
        enumeration_sol_lst = []
        for model in enumeration_sol:
            logger.info('Completion ' + str(count) + ':')
            count += 1
            model_lst = model.to_list()
            enumeration_sol_lst.append(model_lst)
            utils.print_met(model_lst)
        #TODO provide clean lists, not list version of terms in what is returned
    return unprod_lst, reconstructable_targets, one_min_sol_lst, intersection_sol_lst, union_sol_lst, enumeration_sol_lst


if __name__ == '__main__':
    cmd_meneco()
