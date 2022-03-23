# Meneco [![PyPI version](https://img.shields.io/pypi/v/meneco.svg)](https://pypi.org/project/meneco/)

## Installation

Requires **Python >= 3.7**

Required packages (starting from version 2.0 of the package):

* [``Clyngor``](https://github.com/Aluriak/clyngor) or [``Clyngor_with_clingo``](https://github.com/Aluriak/clyngor-with-clingo) that includes the solvers

You can install Meneco by running:

```sh
python setup.py install
```

You should always use a virtual environment ([virtualenv](https://virtualenv.pypa.io/en/latest/), [virtualenv wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)) when using Python

## Usage from console

Typical usage is:

```sh
meneco -d draftnetwork.sbml -s seeds.sbml -t targets.sbml -r repairnetwork.sbml
```

For more options you can ask for help as follows:

```text
usage: meneco [-h] -d DRAFTNET -s SEEDS -t TARGETS [-r REPAIRNET]
                   [--enumerate] [--json]

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
  --json                produce JSON output
```

## Calling Meneco from a python script

You can use Meneco from python by calling the command run_meneco() with the paths of files as input arguments and a boolean value for the enumeration (`True` for the enumeration, else `False`) :

```py
from meneco import run_meneco

result = run_meneco(draftnet="toy/draft.sbml",
                seeds="toy/seeds.sbml",
                targets="toy/targets.sbml",
                repairnet="toy/repair.sbml",
                enumeration=False,
                json=True)
```

The output will be the set of unproducible targets, reconstructable targets, a dictionnary of essentials reactions for each target, one minimal solution, the set of reactions belonging to the intersection of solutions, the set of reactions belonging to the union of solutions and a list of lists corresponding to the reactions for each solution (if enumeration == True).

For a step by step demonstration on how to use Meneco as a library, have a look at our notebooks [here](https://mybinder.org/v2/gh/bioasp/meneco/master?filepath=meneco.ipynb) or [here](https://colab.research.google.com/drive/170IQ8YV-J0R1GH6rsU2t8YUKOkApLeNF?usp=sharing).

## Bibliography

Please cite the following paper when using Meneco:

**S. Prigent et al., “Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks,” PLOS Computational Biology, vol. 13, no. 1, p. e1005276, Jan. 2017. [https://doi.org/10.1371/journal.pcbi.1005276](https://doi.org/10.1371/journal.pcbi.1005276)**

The concepts underlying Meneco is described in this paper:

T. Schaub and S. Thiele, “Metabolic network expansion with answer set programming,” in Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics), 2009, vol. 5649 LNCS, pp. 312–326. [https://doi.org/10.1007/978-3-642-02846-5_27](https://doi.org/10.1007/978-3-642-02846-5_27)

A first application of the method was presented in:

G. Collet et al., “Extending the Metabolic Network of Ectocarpus Siliculosus Using Answer Set Programming,” in LPNMR 2013: Logic Programming and Nonmonotonic Reasoning, 2013, pp. 245–256. [https://doi.org/10.1007/978-3-642-40564-8_25](https://doi.org/10.1007/978-3-642-40564-8_25)

## Samples

Sample files for the reconstruction of Ectocarpus are available here: [ectocyc.sbml][1], [metacyc_16-5.sbml][2], [seeds.sbml][3], [targets.sbml][4]

[1]: http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml
[2]: http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml
[3]: http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml
[4]: http://bioasp.github.io/downloads/samples/ectodata/targets.sbml
