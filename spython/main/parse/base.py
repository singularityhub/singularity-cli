
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

from spython.logger import bot
from spython.utils import ( read_file, write_file )


class Recipe(object):
    '''a recipe includes an environment, labels, runscript or command,
       and install sequence. This object is interacted with by a Parser 
       (intended to popualte the recipe with content) and a Writer (intended
       to write a recipe to file). The parsers and writers are located in
       parsers.py, and writers.py, respectively. The user is also free to use
       the recipe class to build recipes.

       Parameters
       ==========
       recipe: the original recipe file, parsed by the subclass either
               DockerRecipe or SingularityRecipe

    '''

    def __init__(self, recipe=None):

        self.cmd = None
        self.comments = []
        self.entrypoint = None
        self.environ = []
        self.files = []
        self.install = []
        self.labels = []
        self.ports = []
        self.test = None
        self.volumes = []
        self.workdir = None

        self.source = recipe

    def __str__(self):
        ''' show the user the recipe object, along with the type. E.g.,
       
            [spython-recipe][source:Singularity]
            [spython-recipe][source:Dockerfile]

        '''
        base = "[spython-recipe]"
        if self.source:
            base = "%s[source:%s]" %(base, self.source)
        return base

    def __repr__(self):
        return self.__str__()
