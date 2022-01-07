# Copyright (c) 2014, Sven Thiele <sthiele78@gmail.com>
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
import re
from clyngor import as_pyasp
from clyngor.as_pyasp import TermSet, Atom
import xml.etree.cElementTree as etree
from xml.etree.cElementTree import XML, fromstring, tostring
import logging

logger = logging.getLogger(__name__)


def get_model(sbml):
    model_element = None
    for e in sbml:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "model":
            model_element = e
            break
    return model_element


def get_listOfSpecies(model):
    listOfSpecies = None
    for e in model:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfSpecies":
            listOfSpecies = e
            break
    return listOfSpecies


def get_listOfReactions(model):
    listOfReactions = None
    for e in model:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfReactions":
            listOfReactions = e
            break
    return listOfReactions


def get_listOfReactants(reaction):
    listOfReactants = None
    for e in reaction:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfReactants":
            listOfReactants = e
            break
    return listOfReactants


def get_listOfProducts(reaction):
    listOfProducts = None
    for e in reaction:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "listOfProducts":
            listOfProducts = e
            break
    return listOfProducts


def get_score(reaction):
    score = 0
    for e in reaction:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "annotation":
            for s in e:
                if s.tag[0] == "{":
                    _uri, stag = s.tag[1:].split("}")
                else:
                    stag = s.tag
                if stag == "score":
                    score = s.attrib.get("val")
    return score


def readSBMLnetwork(filename, name):

    lpfacts = TermSet()
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)
    listOfReactions = get_listOfReactions(model)

    for e in listOfReactions:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "reaction":
            reactionId = e.attrib.get("id")
            lpfacts.add(Atom("reaction", ['"' + reactionId + '"', '"' + name + '"']))
            if e.attrib.get("reversible") == "true":
                lpfacts.add(
                    Atom("reversible", ['"' + reactionId + '"', '"' + name + '"'])
                )

            listOfReactants = get_listOfReactants(e)
            if listOfReactants == None:
                logger.warning("Warning: {0} listOfReactants=None".format(reactionId))
            else:
                for r in listOfReactants:
                    lpfacts.add(
                        Atom(
                            "reactant",
                            [
                                '"' + r.attrib.get("species") + '"',
                                '"' + reactionId + '"',
                                '"' + name + '"',
                            ],
                        )
                    )

            listOfProducts = get_listOfProducts(e)
            if listOfProducts == None:
                logger.warning("Warning: {0} listOfProducts=None".format(reactionId))
            else:
                for p in listOfProducts:
                    lpfacts.add(
                        Atom(
                            "product",
                            [
                                '"' + p.attrib.get("species") + '"',
                                '"' + reactionId + '"',
                                '"' + name + '"',
                            ],
                        )
                    )

    if name == "draft":
        lpfacts.add(Atom("draft", ['"' + name + '"']))

    return lpfacts


def readSBMLnetwork_with_score(filename, name):

    lpfacts = TermSet()
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)
    listOfReactions = get_listOfReactions(model)

    for e in listOfReactions:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "reaction":
            reactionId = e.attrib.get("id")
            lpfacts.add(Atom("reaction", ['"' + reactionId + '"', '"' + name + '"']))
            if e.attrib.get("reversible") == "true":
                lpfacts.add(
                    Atom("reversible", ['"' + reactionId + '"', '"' + name + '"'])
                )

            listOfReactants = get_listOfReactants(e)
            if listOfReactants == None:
                logger.warning("Warning: {0} listOfReactants=None".format(reactionId))
            else:
                for r in listOfReactants:
                    lpfacts.add(
                        Atom(
                            "reactant",
                            [
                                '"' + r.attrib.get("species") + '"',
                                '"' + reactionId + '"',
                                '"' + name + '"',
                            ],
                        )
                    )

            listOfProducts = get_listOfProducts(e)
            if listOfProducts == None:
                logger.warning("Warning: {0} listOfProducts=None".format(reactionId))
            else:
                for p in listOfProducts:
                    lpfacts.add(
                        Atom(
                            "product",
                            [
                                '"' + p.attrib.get("species") + '"',
                                '"' + reactionId + '"',
                                '"' + name + '"',
                            ],
                        )
                    )

            score = get_score(e)
            if score != 0:
                value = int(float(score) * 1000)
                lpfacts.add(Atom("value", ['"' + reactionId + '"', str(value)]))
            else:
                # print " no value for ",Reaction_ID
                lpfacts.add(Atom("value", ['"' + reactionId + '"', "0"]))

    if name == "draft":
        lpfacts.add(Atom("draft", ['"' + name + '"']))

    return lpfacts


def readSBMLtargets(filename):

    lpfacts = TermSet()
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)
    listOfSpecies = get_listOfSpecies(model)

    for e in listOfSpecies:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "species":
            lpfacts.add(Atom("target", ['"' + e.attrib.get("id") + '"']))
    return lpfacts


def readSBMLseeds(filename):
    lpfacts = TermSet()
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)
    listOfSpecies = get_listOfSpecies(model)

    for e in listOfSpecies:
        if e.tag[0] == "{":
            _uri, tag = e.tag[1:].split("}")
        else:
            tag = e.tag
        if tag == "species":
            lpfacts.add(Atom("seed", ['"' + e.attrib.get("id") + '"']))
    return lpfacts
