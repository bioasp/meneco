# **Meneco** User Guide (version 2.0.2-dev)

Sven Thiele

## What is Meneco

Meneco is a tool for metabolic network completion.
Within a qualitative approach that describes the bio-synthetic capacities of metabolic networks,
Meneco uses qualitative constraints to express the producibility for a set of metabolites.
Meneco can be used to check whether a network provides the synthesis routes to comply
with the required functionality described by the producibility constraints.
In particular it tests whether it is possible to synthesize so called target metabolites from a set of seed metabolites.

For networks that fail this test Meneco can attempt to complete the network by importing reactions
from a metabolic reference network such that the resulting network provides the required functionality.
Meneco can identify unproducible target metabolites and computes minimal extensions to the network that satisfy the producibility constraints.
Additionally, it can compute the union and intersection of all minimal networks extensions without enumerating all minimal network extensions.

## Prerequisites

Meneco is a Python application that uses the power of answer set solving technology to compute its solution.
Therefore it depends on the [`Clyngor`](https://github.com/Aluriak/clyngor-with-clingo) library, a python wrapper for the solvers from the [Potassco Answer Set Solving Collection](https://potassco.org).
All dependencies are automatically resolved and installed via `pip`, the recommended package installer for the Python Package index where the software is hosted.
Meneco runs on the Linux and Mac OS operating systems Windows is currently **not supported**.

## Installation using `pip`

You can install the `meneco` package by running:

```sh
pip install --user meneco
```

On Linux the executable scripts can then be found in `~/.local/bin`

and on Mac OS the scripts are under `/Users/YOURUSERNAME/Library/Python/3.6/bin`.

## Usage from the Command line

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

## Input

Meneco works with two kinds of data.
The first is metabolic reaction data representing metabolic reactions from the draft network and the reference database (i.e. the metacyc db).
The second is the information about seed and target metabolites.

### Metabolic reaction data

The metabolic reaction data must be presented in Systems Biology Markup Language format `SBML} as shown below.

Here is how one could represent a metabolic reaction network in SBML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sbml level="2" version="3" xmlns="http://www.sbml.org/sbml/level2/version3">
    <model name="EnzymaticReaction">
        <listOfCompartments>
            <compartment id="cytosol" size="1e-14"/>
        </listOfCompartments>
        <listOfSpecies>
            <species compartment="cytosol" id="ES" initialAmount="0"     name="ES"/>
            <species compartment="cytosol" id="P"  initialAmount="0"     name="P"/>
            <species compartment="cytosol" id="S"  initialAmount="1e-20" name="S"/>
            <species compartment="cytosol" id="E"  initialAmount="5e-21" name="E"/>
        </listOfSpecies>
        <listOfReactions>
            <reaction id="veq">
                <listOfReactants>
                    <speciesReference species="E"/>
                    <speciesReference species="S"/>
                </listOfReactants>
                <listOfProducts>
                    <speciesReference species="ES"/>
                </listOfProducts>
            </reaction>
            <reaction id="vcat" reversible="true">
                <listOfReactants>
                    <speciesReference species="ES"/>
                </listOfReactants>
                <listOfProducts>
                    <speciesReference species="E"/>
                    <speciesReference species="P"/>
                </listOfProducts>
            </reaction>
        </listOfReactions>
    </model>
</sbml>
```

In this example, the model has the identifier `EnzymaticReaction`.
The model contains one compartment (with identifier `cytosol`),
four metabolites (with species identifiers `ES`, `P`, `S`, and `E`), and two reactions (`veq` and `vcat`).
The elements in the `listOfReactants` and `listOfProducts` in each reaction refer to the names of elements listed in the `listOfSpecies`.
The correspondences between the various elements is explicitly stated by the `speciesReference` elements.
The reaction `vcat` has the attribute `reversible` set to `true`.
Note that `meneco` will only treat a reaction as reversible if this attribute is set to `true`.
If the attribute is not set, the default assumption is that a reaction is irreversible.
Thus, the reaction `veq` is treated as irreversible.
The SBML file may contain additional informations (like `initialAmount="1e-20"`) which will be ignored by Meneco.

### Seed and Target data

Also information about seed and target metabolites can be specified using SBML files.
For convenience reasons Meneco takes two files one which presents the specification of the seed metabolites and one file for the target metabolites.
Here is how such a file could look like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sbml level="2" version="3" xmlns="http://www.sbml.org/sbml/level2/version3">
<model id="enzreact_ntrexp_001" name="set of seed metabolites 1">
<listOfSpecies>
    <species id="E" name="This crazy metabolite E"/>
    <species id="S" name="This funky metabolite S"/>
</listOfSpecies>
</model>
</sbml>
```

In this example two metabolites (with identifiers E and S) are specified.
It is important that these identifiers match with the identifiers in the description of the reaction network.
Depending on whether this description is passed as 3rd or 4th argument Meneco regards the specified metabolites as seeds resp. targets.

## Output

If you do not set the flag `--json` the result is written in markdown like format to stdout.

The output of Meneco can be redirected into a file using the `>` operator.
For example to write the results shown below into the file `result.md` type:

```sh
meneco.py -d draftnet.sbml -s seeds.sbml -t targets.sbml -r repairdb.sbml --enumerate > result.md
```

While Meneco is running you get some status messages about what it does.

```text
Reading draft network ...
Reading seeds ...
Reading targets ...
Checking draftnet for unproducible targets
Reading repair db ...
Checking draftnet + repairnet for unproducible targets
Computing essential reactions for M_cu2_c
Computing essential reactions for M_cl_c
Adding essential reactions to network
Computing one minimal completion to produce all targets
Computing common reactions in all completion with size 3
Computing union of reactions from all completion with size 3
Computing all completions with size 3
```

In the following we will dissect the output generated by Meneco.

```text
Draft network file: draftnet.sbml
Seeds file: seeds.sbml
Targets file: targets.sbml
```

The first 3 lines document which files have been used as the metabolic reaction network
and to specify the seeds and targets.

```text
7 unproducible targets:
    M_so4_c
    M_cl_c
    M_cu2_c
    M_pe161_c
    M_thf_c
    M_ribflv_c
    M_utp_c
```

In this section Meneco outputs which target metabolite are producible given the seeds and the reactions of the draft network.
In this case the result shows 7 target metabolites which are not producible.

Given that unproducible target metabolites exist the next sections documents which of the targets remain unproducible even with the reactions from the repair database `repairdb.sbml`
and for which targets the metabolic pathways can be reconstructed.

```text
Repair db file: repairdb.sbml

Still 5 unreconstructable targets:
    M_so4_c
    M_pe161_c
    M_utp_c
    M_ribflv_c
    M_thf_c

2 reconstructable targets:
    M_cu2_c
    M_cl_c
```

In this example 5 metabolites remain unproducible,
but for 2 targets Meneco is able to repair the synthesis pathways.

As a precomputation step Meneco reconstruct the production pathways for each single reconstructable target metabolite, and computing the essential reactions.
Essential reaction in this context are reactions which always must be added to allow a synthesis of the target from the seeds.
This intermediate result is reused in the subsequent computations as a solution that restores all targets must contain all reaction that are essential for each single target.

```text
1 essential reactions for target M_cu2_c:
    R_CU2tpp

1 essential reactions for target M_cl_c:
    R_CLt3_2pp

Overall 2 essential reactions found:
    R_CU2tpp
    R_CLt3_2pp
```

In this example for each single target metabolite exist one essential reaction.

The section shows one minimal completion to produce all targets.

```text
One minimal completion of size 3:
    R_O2Stex
    R_CU2tpp
    R_CLt3_2pp
```

In this example the first minimal completion contains 3 reactions.

Given the size of a minimal completion.s.
Meneco outputs the intersection and union of all minimal completion

```text
Intersection of cardinality minimal completions:
    R_CU2tpp
    R_CLt3_2pp

Union of cardinality minimal completions:
    R_O2tex
    R_O2Stex
    R_CU2tpp
    R_CLt3_2pp
```

In our case we get 2 reactions in the intersection and 4 reactions in the union.

Finally, if the command line option `--enumerate` has been given,
all minimal completions are enumerated.

```text
Completion 1:
    R_O2Stex
    R_CU2tpp
    R_CLt3_2pp

Completion 2:
    R_O2tex
    R_CU2tpp
    R_CLt3_2pp
```

Fortunately, our example has only two solutions.
In general the number of solutions can be very high.
Therfore, enumeration is only done if explicitly requested via command line option.

## References

* *Meneco, a Topology-Based Gap-Filling Tool Applicable to Degraded Genome-Wide Metabolic Networks.* (2017). PLOS Computational Biology. [DOI](http://dx.doi.org/10.1371/journal.pcbi.1005276)

* *The genome-scale metabolic network of Ectocarpus siliculosus (EctoGEM): a resource to study brown algal physiology and beyond.* (2014). The Plant Journal. [DOI](http://dx.doi.org/10.1111/tpj.12627)

* *Extending the Metabolic Network of Ectocarpus Siliculosus using Answer Set Programming.* (2013). 12th International Conference on Logic Programming and Nonmonotonic Reasoning. [DOI](http://dx.doi.org/10.1007/978-3-642-40564-8_25)

* *Metabolic Network Expansion with Answer Set Programming.* (2009). 25th International Conference on Logic Programming. [DOI](http://dx.doi.org/10.1007/978-3-642-02846-5_27)
