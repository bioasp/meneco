---
layout: index
title: meneco
tagline: A tool for the completion of metabolic networks
---

### Metabolic network completion

Large-scale metabolic networks as well as measured data sets suffer from substantial incompleteness. 
meneco is a tool for metabolic network completion. It can be used to check whether a network provides the synthesis routes to comply with the required functionality described by the producibility of metabolites. 
In particular, it tests whether it is possible to synthesize so called target metabolites from a set of seed metabolites. For networks that fail this test meneco can attempt to complete the network by importing reactions from a metabolic reference database such that the resulting network provides the required functionality.
meneco can identify unproducible target metabolites and computes minimal extensions to the network that satisfy the producibility constraints. Additionally, it can compute the union and intersection of all minimal networks extensions without enumerating all minimal network extensions. meneco builds upon a formal method for analyzing large-scale metabolic networks. This qualitative approach describes the bio-synthetic capacities of metabolic networks.
Implementing this approach, meneco maps its principles into Answer Set Programming to express the producibility constraints for a set of metabolites.


### Installation 

You can install meneco by running:

	$ pip install --user meneco

On Linux the executable script can then be found in ``~/.local/bin``

and on MacOS the script is under ``/Users/YOURUSERNAME/Library/Python/3.2/bin``.


### Usage of Command line interface

You can download the [meneco user guide](https://bioasp.github.io/meneco/guide/guide.pdf).
Typical usage is:

```sh
meneco -d draftnetwork.sbml -s seeds.sbml -t targets.sbml -r repairnetwork.sbml
```

For more options you can ask for help as follows:

```sh
meneco --h
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
```


### Usage of library

For a guided example, see a [demonstration IPython Notebook](http://nbviewer.jupyter.org/github/bioasp/meneco/blob/master/meneco.ipynb).


### Samples

Sample files for the reconstruction of ectocarpus are available here:
      [ectocyc.sbml](http://bioasp.github.io/downloads/samples/ectodata/ectocyc.sbml), [metacyc_16-5.sbml](http://bioasp.github.io/downloads/samples/ectodata/metacyc_16-5.sbml), [seeds.sbml](http://bioasp.github.io/downloads/samples/ectodata/seeds.sbml), [targets.sbml](http://bioasp.github.io/downloads/samples/ectodata/targets.sbml).


### Related publications

* *Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks.* (2017). PLOS Computational Biology. [DOI](http://dx.doi.org/10.1371/journal.pcbi.1005276)

* *The genome-scale metabolic network of Ectocarpus siliculosus (EctoGEM): a resource to study brown algal physiology and beyond.* (2014). The Plant Journal. [DOI](http://dx.doi.org/10.1111/tpj.12627)


* *Extending the Metabolic Network of Ectocarpus Siliculosus using Answer Set Programming.* (2013). 12th International Conference on Logic Programming and Nonmonotonic Reasoning. [DOI](http://dx.doi.org/10.1007/978-3-642-40564-8_25)

* *Metabolic Network Expansion with Answer Set Programming.* (2009). 25th International Conference on Logic Programming. [DOI](http://dx.doi.org/10.1007/978-3-642-02846-5_27)
