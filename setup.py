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
from setuptools import setup
                         
setup(
  name             = 'meneco',
  version          = '1.5.0',
  url              = 'http://bioasp.github.io/meneco/',
  license          = 'GPLv3+',
  description      = 'Metabolic Network Completion. Compute minimal completions '
                     'to your draft network with reactions from a repair network.',
  long_description = open('README.rst').read(),
  author           = 'Sven Thiele',
  author_email     = 'sthiele78@gmail.com',
  packages         = ['__meneco__'],
  package_dir      = {'__meneco__' : 'src'},
  package_data     = {'__meneco__' : ['encodings/*.lp']},
  scripts          = ['meneco.py'],
  install_requires = ['pyasp == 1.4.2']
)
