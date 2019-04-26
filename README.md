# Installation

You can install meneco by running:

    > pip install --user meneco

On Linux the executable script can then be found in `~/.local/bin`

and on MacOS the script is under `/Users/YOURUSERNAME/Library/Python/3.2/bin`.


# Usage Command line interface

Typical usage is:

    > meneco -d draftnetwork.sbml -s seeds.sbml -t targets.sbml -r repairnetwork.sbml

For more options you can ask for help as follows:

    > meneco --h
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


# Usage Library

For a guided example, see a demonstration IPython [Notebook](http://nbviewer.jupyter.org/github/bioasp/meneco/blob/master/meneco.ipynb).


# Bibliography

Please cite the following paper when using Meneco

S. Prigent et al., “Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks,” PLOS Computational Biology, vol. 13, no. 1, p. e1005276, Jan. 2017.


# Samples

Sample files for the reconstruction of ectocarpus are available here: [ectocyc.sbml][1], [metacyc_16-5.sbml][2], [seeds.sbml][3], [targets.sbml][4]

[1]: http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml
[2]: http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml
[3]: http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml
[4]: http://bioasp.github.io/downloads/samples/ectodata/targets.sbml
