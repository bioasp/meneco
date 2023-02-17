---
layout: index
title: Meneco
tagline: A tool for the completion of metabolic networks
---

## Metabolic network completion

Large-scale metabolic networks as well as measured data sets suffer from substantial incompleteness.
Meneco is a tool for metabolic network completion.
It can be used to test whether a network can synthesize so called target metabolites from a set of seed metabolites.
Meneco identifies unproducible targets and can attempt to complete missing synthesis routes by extending the metabolic network with reactions from a reference database such that the resulting network satisfies the producibility constraints.

While Meneco can be used to enumerate all minimal extensions, it can also compute the union and intersection of all minimal networks extensions without enumerating all minimal network extensions.

The methods implemented in Meneco are based on a formal description of the qualitative bio-synthetic capacities of metabolic networks.
Menoco uses Answer Set Programming to express the principles of this formalism and thus the producibility constraints for a set of metabolic reactions.

## Installation

You can install Meneco by running:

```sh
pip install --user meneco
```

On Linux the executable script can then be found in ``~/.local/bin``

and on MacOS the script is under ``/Users/YOURUSERNAME/Library/Python/3.6/bin``.

## Usage of Command line interface

You can download the [Meneco User Guide](https://bioasp.github.io/meneco/guide/guide.html).
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

## Usage as a library

You can use Meneco from python by calling the command `run_meneco()` with the paths of files as input arguments and a boolean value for the enumeration (`True` for the enumeration, else `False`) :

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

## Samples

Sample files for the reconstruction of ectocarpus are available here:
      [ectocyc.sbml](http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml), [metacyc_16-5.sbml](http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml), [seeds.sbml](http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml), [targets.sbml](http://bioasp.github.io/downloads/samples/ectodata/targets.sbml).

## Related publications

* *Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks.* (2017). PLOS Computational Biology. [DOI](http://dx.doi.org/10.1371/journal.pcbi.1005276)

* *The genome-scale metabolic network of Ectocarpus siliculosus (EctoGEM): a resource to study brown algal physiology and beyond.* (2014). The Plant Journal. [DOI](http://dx.doi.org/10.1111/tpj.12627)

* *Extending the Metabolic Network of Ectocarpus Siliculosus using Answer Set Programming.* (2013). 12th International Conference on Logic Programming and Nonmonotonic Reasoning. [DOI](http://dx.doi.org/10.1007/978-3-642-40564-8_25)

* *Metabolic Network Expansion with Answer Set Programming.* (2009). 25th International Conference on Logic Programming. [DOI](http://dx.doi.org/10.1007/978-3-642-02846-5_27)
