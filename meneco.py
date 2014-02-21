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
from pyasp.asp import *
import argparse
from __meneco__ import query, utils, sbml

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("draftnetwork",
                        help="metabolic network in SBML format")
    parser.add_argument("repairnetwork",
                        help="metabolic network in SBML format")     
    parser.add_argument("seeds",
                        help="seeds in SBML format") 
    parser.add_argument("targets",
                        help="targets in SBML format") 

    parser.add_argument('--enumerate', 
			help="enumerate all minimal completions",
			action="store_true")
    
    args = parser.parse_args()        
        
    draft_sbml = args.draftnetwork
    repair_sbml = args.repairnetwork
    seeds_sbml = args.seeds
    targets_sbml =  args.targets
    
    print 'Reading draft network from ',draft_sbml,'...',
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft')
    print 'done.'
    #draftnet.to_file("draftnet.lp")
    
    print 'Reading seeds from ',seeds_sbml,'...',
    seeds = sbml.readSBMLseeds(seeds_sbml)
    print 'done.'
    #seeds.to_file("seeds.lp")
        
    print 'Reading targets from ',targets_sbml,'...',
    targets = sbml.readSBMLtargets(targets_sbml)
    print 'done.'
    #targets.to_file("targets.lp")

    print '\nChecking draftnet for unproducible targets ...',
    model = query.get_unproducible(draftnet, targets, seeds)
    print 'done.'
    print ' ',len(model),'unproducible targets:'
    utils.print_met(model.to_list())
    unproducible_targets = TermSet()
    for a in model :
      target= str(a)[13:]
      t = String2TermSet(target)
      unproducible_targets = unproducible_targets.union(t)
      
    print '\nReading repair network from ',repair_sbml,'...',
    repairnet = sbml.readSBMLnetwork(repair_sbml, 'repairnet')
    print 'done.'
    #repairnet.to_file("repairnet.lp")


    all_reactions = draftnet
    all_reactions = all_reactions.union(repairnet)
    print '\nChecking draftnet + repairnet for unproducible targets ...',
    model = query.get_unproducible(all_reactions, seeds, targets)
    print 'done.'
    print '  still',len(model),'unproducible targets:'
    utils.print_met(model.to_list())
    never_producible = TermSet()
    for a in model :
      target= str(a)[13:]
      t = String2TermSet(target)
      never_producible = never_producible.union(t)

    reconstructable_targets = TermSet()
    for t in unproducible_targets:
      if not (t in never_producible) :      reconstructable_targets.add(t)
    print '\n ',len(reconstructable_targets),'targets to reconstruct:'
    utils.print_met(reconstructable_targets)

    if len(reconstructable_targets)== 0 :
      utils.clean_up()
      quit()
      
      
    essential_reactions = TermSet()
    for t in reconstructable_targets:
      single_target = TermSet()
      single_target.add(t)
      print '\nComputing essential reactions for',t,'...',
      essentials =  query.get_intersection_of_completions(draftnet, repairnet, seeds, single_target)
      print 'done.'
      print ' ',len(essentials), 'essential reactions found:'
      utils.print_met(essentials.to_list())
      essential_reactions = essential_reactions.union(essentials)
    print '\n  Overall',len(essential_reactions), 'essential reactions found.'
    utils.print_met(essential_reactions)
    print '\n Add essential reactions to network.'
    draftnet  = draftnet.union(essential_reactions) 

    utils.clean_up()
    
    
    #draftnet.to_file("draft.lp")
    #repairnet.to_file("repairnet.lp")
    #unproducible_targets.to_file("targets.lp")
    #seeds.to_file("seeds.lp")
    
    print '\nComputing one minimal completion to produce all targets ...',
    models =  query.get_minimal_completion_size(draftnet, repairnet, seeds, reconstructable_targets)
    print 'done.'
    optimum = models[0].score[0]
    utils.print_met(models[0].to_list())

    
    print '\nComputing common reactions in all completion with size',optimum,'...',
    model =  query.get_intersection_of_optimal_completions(draftnet, repairnet, seeds, reconstructable_targets,  optimum)
    print 'done.'
    utils.print_met(model.to_list())
    
    print '\nComputing union of reactions from all completion with size',optimum,'...',
    model =  query.get_union_of_optimal_completions(draftnet, repairnet, seeds, reconstructable_targets, optimum)
    print 'done.'
    utils.print_met(model.to_list())

    if args.enumerate :
      print '\nComputing all completions with size',optimum,'...',
      models =  query.get_optimal_completions(draftnet, repairnet, seeds, reconstructable_targets, optimum)
      print 'done.'
      count = 1
      for model in models:
	print 'Completion '+str(count)+':'
	count+=1
        utils.print_met(model.to_list())

