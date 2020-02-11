# Installation

You can install meneco by running:

    > python setup.py install

You should always use a virtual environment ([https://virtualenv.pypa.io/en/latest/](virtualenv), [https://virtualenvwrapper.readthedocs.io/en/latest/](virtualenv wrapper)) when using Python


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

Please cite the following paper when using Meneco:

**S. Prigent et al., “Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks,” PLOS Computational Biology, vol. 13, no. 1, p. e1005276, Jan. 2017.**

The concepts underlying Meneco is described in this paper:

T. Schaub and S. Thiele, “Metabolic network expansion with answer set programming,” in Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics), 2009, vol. 5649 LNCS, pp. 312–326.

A first application of the method was presented in:

G. Collet et al., “Extending the Metabolic Network of Ectocarpus Siliculosus Using Answer Set Programming,” in LPNMR 2013: Logic Programming and Nonmonotonic Reasoning, 2013, pp. 245–256.


# Samples

Sample files for the reconstruction of ectocarpus are available here: [ectocyc.sbml][1], [metacyc_16-5.sbml][2], [seeds.sbml][3], [targets.sbml][4]

[1]: http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml
[2]: http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml
[3]: http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml
[4]: http://bioasp.github.io/downloads/samples/ectodata/targets.sbml
