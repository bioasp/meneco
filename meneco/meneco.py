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
from clyngor.as_pyasp import TermSet, Atom
from clyngor import as_pyasp
import clyngor
import argparse
import sys
import json
import logging
from meneco import utils, sbml, query

logger = logging.getLogger(__name__)


def cmd_meneco(argv):
    """Run meneco from shell
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--draftnet", help="metabolic network in SBML format", required=True
    )
    parser.add_argument("-s", "--seeds", help="seeds in SBML format", required=True)
    parser.add_argument("-t", "--targets", help="targets in SBML format", required=True)

    parser.add_argument(
        "-r",
        "--repairnet",
        help="perform network completion using REPAIRNET "
        "a metabolic network in SBML format",
    )

    parser.add_argument(
        "--enumerate",
        help="enumerate all minimal completions",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--json",
        help="produce JSON output",
        required=False,
        action="store_true",
        default=False,
    )

    args = parser.parse_args(argv)

    result = run_meneco(
        args.draftnet,
        args.seeds,
        args.targets,
        args.repairnet,
        args.enumerate,
        args.json,
    )
    if args.json:
        print(json.dumps(result, indent=4))


def extract_xreactions(model, return_atom=True):
    lst = set(a[0] for pred in model if pred == "xreaction" for a in model[pred])
    if return_atom:
        atom = TermSet(
            Atom('xreaction("' + a[0] + '","' + a[1] + '")')
            for pred in model
            if pred == "xreaction"
            for a in model[pred]
        )
        return lst, atom
    else:
        return lst


def extract_unprod_target(model):
    return set(
        a[0] for pred in model if pred == "unproducible_target" for a in model[pred]
    )


def run_meneco(
    draftnet: str,
    seeds: str,
    targets: str,
    repairnet: str,
    enumeration: bool,
    json: bool,
):
    """Complete metabolic network by selecting reactions from a database

    Args:
        draftnet: SBML file name of metabolic network
        seeds: SBML file name seeds
        targets: SBML file name of targets
        repairnet: SBML file name of repair database
    """
    result = {}

    logger.info("Reading draft network ...")
    result["Draft network file"] = draftnet
    if not json:
        print("Draft network file: {0}".format(draftnet))
    draftnet = sbml.readSBMLnetwork(draftnet, "draft")
    # draftnet.to_file("draftnet.lp")

    logger.info("Reading seeds ...")
    result["Seeds file"] = seeds
    if not json:
        print("Seeds file: {0}".format(seeds))
    seeds = sbml.readSBMLseeds(seeds)
    # seeds.to_file("seeds.lp")

    logger.info("Reading targets ...")
    result["Targets file"] = targets
    if not json:
        print("Targets file: {0}\n".format(targets))
    targets = sbml.readSBMLtargets(targets)
    # targets.to_file("targets.lp")

    logger.info("Checking draftnet for unproducible targets ...")
    model = query.get_unproducible(draftnet, seeds, targets)

    unproducible_targets_lst = extract_unprod_target(model)

    result["Unproducible targets"] = list(unproducible_targets_lst)
    if not json:
        print(
            "{0} unproducible targets:\n    {1}\n".format(
                len(unproducible_targets_lst), "\n    ".join(unproducible_targets_lst)
            )
        )

    if len(unproducible_targets_lst) == 0:
        utils.clean_up()
        return result

    if repairnet == None:
        utils.clean_up()
        return result

    logger.info("Reading repair db ...")
    result["Repair db file"] = repairnet
    if not json:
        print("Repair db file: {0}\n".format(repairnet))
    repairnet = sbml.readSBMLnetwork(repairnet, "repairnet")
    # repairnet.to_file("repairnet.lp")

    all_reactions = draftnet
    all_reactions = TermSet(all_reactions.union(repairnet))
    logger.info("Checking draftnet + repairnet for unproducible targets ...")
    model = query.get_unproducible(all_reactions, seeds, targets)
    never_producible = extract_unprod_target(model)

    result["Unreconstructable targets"] = list(never_producible)
    if not json:
        print(
            "Still {0} unreconstructable targets:\n    {1}\n".format(
                len(never_producible), "\n    ".join(never_producible)
            )
        )

    reconstructable_targets = set()
    reconstructable_targets_atoms = TermSet()
    for t in unproducible_targets_lst:
        if not (t in never_producible):
            reconstructable_targets.add(t)
            reconstructable_targets_atoms.add(Atom('target("' + t + '")'))

    result["Reconstructable targets"] = list(reconstructable_targets)
    if not json:
        print(
            "{0} reconstructable targets:\n    {1}\n".format(
                len(reconstructable_targets), "\n    ".join(reconstructable_targets)
            )
        )

    if len(reconstructable_targets) == 0:
        utils.clean_up()
        return result

    essential_reactions = TermSet()
    essential_reactions_to_print = set()
    essential_reactions_target = {}
    for t in reconstructable_targets:
        single_target = TermSet()
        single_target.add(Atom('target("' + t + '")'))
        logger.info(f"Computing essential reactions for {t} ...")
        essentials = query.get_intersection_of_completions(
            draftnet, repairnet, seeds, single_target
        )

        essentials_to_print, essentials_atoms = extract_xreactions(essentials, True)

        essential_reactions_target[t] = list(essentials_to_print)
        if not json:
            print(
                "{0} essential reactions for target {1}:\n    {2}\n".format(
                    len(essentials_to_print), t, "\n    ".join(essentials_to_print)
                )
            )

        essential_reactions = TermSet(essential_reactions.union(essentials_atoms))
        essential_reactions_to_print = set(
            essential_reactions_to_print.union(essentials_to_print)
        )

    result["Essential reactions"] = essential_reactions_target
    if not json:
        print(
            "Overall {0} essential reactions found:\n    {1}\n".format(
                len(essential_reactions_to_print),
                "\n    ".join(essential_reactions_to_print),
            )
        )

    logger.info("Adding essential reactions to network!")
    draftnet = TermSet(draftnet.union(essential_reactions))

    utils.clean_up()

    # draftnet.to_file("draft.lp")
    # repairnet.to_file("repairnet.lp")
    # unproducible_targets.to_file("targets.lp")
    # seeds.to_file("seeds.lp")

    logger.info("Computing one minimal completion to produce all targets ...")
    one_min_sol = query.get_minimal_completion_size(
        draftnet, repairnet, seeds, reconstructable_targets_atoms
    )

    one_min_sol_lst = extract_xreactions(one_min_sol, False)
    optimum = len(one_min_sol_lst)

    result["One minimal completion"] = list(one_min_sol_lst)
    if not json:
        print(
            "One minimal completion of size {0}:\n    {1}\n".format(
                len(one_min_sol_lst), "\n    ".join(one_min_sol_lst)
            )
        )

    logger.info(
        "Computing common reactions in all completion with size {0} ...".format(optimum)
    )
    intersection_sol = query.get_intersection_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
    )

    intersection_sol_lst = extract_xreactions(intersection_sol, False)

    result["Intersection of cardinality minimal completions"] = list(
        intersection_sol_lst
    )
    if not json:
        print(
            "Intersection of cardinality minimal completions:\n    {0}\n".format(
                "\n    ".join(intersection_sol_lst)
            )
        )

    logger.info(
        "Computing union of reactions from all completion with size {0} ...".format(
            optimum
        )
    )
    union_sol = query.get_union_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
    )

    union_sol_lst = extract_xreactions(union_sol, False)

    result["Union of cardinality minimal completions"] = list(union_sol_lst)
    if not json:
        print(
            "Union of cardinality minimal completions:\n    {0}\n".format(
                "\n    ".join(union_sol_lst)
            )
        )

    if enumeration:
        logger.info("Computing all completions with size {0} ...".format(optimum))
        enumeration_sol = query.get_optimal_completions(
            draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
        )
        count = 1
        enumeration_sol_lst = []
        for model in enumeration_sol:
            model_lst = extract_xreactions(model, False)
            enumeration_sol_lst.append(list(model_lst))

            if not json:
                print(
                    "Completion {0}:\n    {1}\n".format(count, "\n    ".join(model_lst))
                )
            count += 1
        result["All cardinality minimal completions"] = enumeration_sol_lst

    return result


if __name__ == "__main__":
    cmd_meneco(sys.argv[1:])
