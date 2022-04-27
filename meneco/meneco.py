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

import argparse
import json
import logging
import sys

from clyngor.as_pyasp import Atom, TermSet

from meneco import query, sbml, utils

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
    json_output: bool,
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
    if not json_output:
        print(f"Draft network file: {draftnet}")
    draftnet = sbml.readSBMLnetwork(draftnet, "draft")
    # draftnet.to_file("draftnet.lp")

    logger.info("Reading seeds ...")
    result["Seeds file"] = seeds
    if not json_output:
        print(f"Seeds file: {seeds}")
    seeds = sbml.readSBMLseeds(seeds)
    # seeds.to_file("seeds.lp")

    logger.info("Reading targets ...")
    result["Targets file"] = targets
    if not json_output:
        print("Targets file: {0}\n".format(targets))
    targets = sbml.readSBMLtargets(targets)
    # targets.to_file("targets.lp")

    logger.info("Checking draftnet for unproducible targets ...")
    model = query.get_unproducible(draftnet, seeds, targets)

    unproducible_targets_lst = list(extract_unprod_target(model))
    unproducible_targets_lst.sort()

    result["Unproducible targets"] = unproducible_targets_lst
    if not json_output:
        print(
            f"{len(unproducible_targets_lst)} unproducible targets"
        )
        if len(unproducible_targets_lst) > 0 :
            print("    {0}\n".format("\n    ".join(unproducible_targets_lst)))
        else: print()


    if len(unproducible_targets_lst) == 0:
        utils.clean_up()
        return result

    if repairnet is None:
        utils.clean_up()
        return result

    logger.info("Reading repair db ...")
    result["Repair db file"] = repairnet
    if not json_output:
        print(f"Repair db file: {repairnet}\n")
    repairnet = sbml.readSBMLnetwork(repairnet, "repairnet")
    # repairnet.to_file("repairnet.lp")

    all_reactions = draftnet
    all_reactions = TermSet(all_reactions.union(repairnet))
    logger.info("Checking draftnet + repairnet for unproducible targets ...")
    model = query.get_unproducible(all_reactions, seeds, targets)
    never_producible = list(extract_unprod_target(model))
    never_producible.sort()

    result["Unreconstructable targets"] = never_producible
    if not json_output:
        print(
            f"{len(never_producible)} unreconstructable targets"
        )
        if len(never_producible) > 0 :
            print("    {0}\n".format("\n    ".join(never_producible)))
        else: print()

    reconstructable_targets = set()
    reconstructable_targets_atoms = TermSet()
    for t in unproducible_targets_lst:
        if not (t in never_producible):
            reconstructable_targets.add(t)
            reconstructable_targets_atoms.add(Atom('target("' + t + '")'))

    reconstructable_targets = list(reconstructable_targets)
    reconstructable_targets.sort()
    result["Reconstructable targets"] = reconstructable_targets
    if not json_output:
        print(
            f"{len(reconstructable_targets)} reconstructable targets"
        )
        if len(reconstructable_targets) > 0 :
            print("    {0}\n".format("\n    ".join(reconstructable_targets)))
        else: print()

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
        essentials_to_print = list(essentials_to_print)
        essentials_to_print.sort()
        essential_reactions_target[t] = essentials_to_print
        if not json_output:
            print(
                f"{len(essentials_to_print)} essential reactions for target {t}"
            )
            if len(essentials_to_print) > 0 :
                print("    {0}\n".format("\n    ".join(essentials_to_print)))
            else: print()

        essential_reactions = TermSet(essential_reactions.union(essentials_atoms))
        essential_reactions_to_print = set(
            essential_reactions_to_print.union(essentials_to_print)
        )

    result["Essential reactions"] = essential_reactions_target
    if not json_output:
        print(
            f"Overall {len(essential_reactions_to_print)} essential reactions found"
        )
        if len(essential_reactions_to_print) > 0 :
            print("    {0}\n".format("\n    ".join(essential_reactions_to_print)))
        else: print()

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

    one_min_sol_lst = list(extract_xreactions(one_min_sol, False))
    one_min_sol_lst.sort()
    optimum = len(one_min_sol_lst)

    result["One minimal completion"] = one_min_sol_lst
    if not json_output:
        print(
            f"One minimal completion of size {len(one_min_sol_lst)}"
        )
        if len(one_min_sol_lst) > 0 :
            print("    {0}\n".format("\n    ".join(one_min_sol_lst)))
        else: print()

    logger.info(
        f"Computing common reactions in all completion with size {optimum} ..."
    )
    intersection_sol = query.get_intersection_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
    )

    intersection_sol_lst = list(extract_xreactions(intersection_sol, False))
    intersection_sol_lst.sort()
    result["Intersection of cardinality minimal completions"] = list(
        intersection_sol_lst
    )
    if not json_output:
        print("Intersection of cardinality minimal completions")
        if len(intersection_sol_lst) > 0 :
            print("    {0}\n".format("\n    ".join(intersection_sol_lst)))
        else: print("    is empty")

    logger.info(
        f"Computing union of reactions from all completion with size {optimum} ..."
    )
    union_sol = query.get_union_of_optimal_completions(
        draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
    )

    union_sol_lst = list(extract_xreactions(union_sol, False))
    union_sol_lst.sort()

    result["Union of cardinality minimal completions"] = union_sol_lst
    if not json_output:
        print("Union of cardinality minimal completions")
        if len(union_sol_lst) > 0 :
            print("    {0}\n".format("\n    ".join(union_sol_lst)))
        else: print("    is empty")

    if enumeration:
        logger.info(f"Computing all completions with size {optimum} ...")
        enumeration_sol = query.get_optimal_completions(
            draftnet, repairnet, seeds, reconstructable_targets_atoms, optimum
        )
        count = 1
        enumeration_sol_lst = []
        for model in enumeration_sol:
            model_lst = extract_xreactions(model, False)
            enumeration_sol_lst.append(list(model_lst))

            if not json_output:
                print(
                    "Completion {0}:\n    {1}\n".format(count, "\n    ".join(model_lst))
                )
            count += 1
        result["All cardinality minimal completions"] = enumeration_sol_lst

    return result


if __name__ == "__main__":
    cmd_meneco(sys.argv[1:])
