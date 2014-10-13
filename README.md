Installation 
============


You can install meneco by running:

	$ pip install --user meneco

The executable scripts can then be found in ~/.local/bin.


Usage
=====

Typical usage is:
	
	$ meneco.py draftnetwork.sbml repairnetwork.sbml seeds.sbml targets.sbml
	
For more options you can ask for help as follows:

	$ meneco --h
	    usage: meneco.py [-h] [--enumerate] draftnetwork repairnetwork seeds targets
	
	    positional arguments:
	      draftnetwork   metabolic network in SBML format
	      repairnetwork  metabolic network in SBML format
	      seeds          seeds in SBML format
	      targets        targets in SBML format
	
	    optional arguments:
	      -h, --help     show this help message and exit
	      --enumerate    enumerate all minimal completions


Samples
=======

Sample files for the reconstruction of ectocarpus are available here:
      [ectocyc.sbml][ectocyc.sbml], [metacyc_16-5.sbml][metacyc_16-5.sbml], [seeds.sbml][seeds.sbml], and [targets.sbml][targets.sbml].

[ectocyc.sbml]: http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml

[metacyc_16-5.sbml]: http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml

[seeds.sbml]: http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml

[targets.sbml]: http://bioasp.github.io/downloads/samples/ectodata/targets.sbml

