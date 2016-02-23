Installation
============


You can install meneco by running::

	$ pip install --user meneco

On Linux the executable script can then be found in ``~/.local/bin``

and on MacOS the script is under ``/Users/YOURUSERNAME/Library/Python/3.2/bin``.


Usage
=====

Typical usage is::

	$ meneco.py -d draftnetwork.sbml -s seeds.sbml -t targets.sbml -r repairnetwork.sbml 

For more options you can ask for help as follows::

        $meneco.py --h
        usage: meneco.py [-h] -d DRAFTNET -s SEEDS -t TARGETS [-r REPAIRNET]
                         [--enumerate]

        optional arguments:
          -h, --help            show this help message and exit
          -d DRAFTNET, --draftnet DRAFTNET
                                metabolic network in SBML format
          -s SEEDS, --seeds SEEDS
                                seeds in SBML format
          -t TARGETS, --targets TARGETS
                                targets in SBML format
          -r REPAIRNET, --repairnet REPAIRNET
                                perform network completion using REPAIRNET a metabolic
                                network in SBML format
          --enumerate           enumerate all minimal completions


Samples
=======

Sample files for the reconstruction of ectocarpus are available here: ectocyc.sbml_, metacyc_16-5.sbml_, seeds.sbml_, targets.sbml_

.. _ectocyc.sbml: http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml
.. _metacyc_16-5.sbml: http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml
.. _seeds.sbml: http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml
.. _targets.sbml: http://bioasp.github.io/downloads/samples/ectodata/targets.sbml
