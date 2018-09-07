
# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.
# Copyright (C) 2017-2018 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys

def main(args, options, parser):

    from spython.main import Client as cli

    # If we have options, first is image
    image = None
    if len(options) > 0:
        image = options.pop(0)
 
    lookup = { 'ipython': ipython,
               'python': python,
               'bpython': bpython }

    shells = ['ipython', 'python', 'bpython']

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](image)
        except ImportError:
            pass
    

def ipython(image):
    '''give the user an ipython shell
    '''

    # The client will announce itself (backend/database) unless it's get
    from spython.main import get_client
    from spython.main.parse import ( DockerRecipe, SingularityRecipe )

    client = get_client()
    client.load(image)

    # Add recipe parsers
    client.DockerRecipe = DockerRecipe
    client.SingularityRecipe = SingularityRecipe

    from IPython import embed
    embed()

def bpython(image):

    import bpython
    from spython.main import get_client
    from spython.main.parse import ( DockerRecipe, SingularityRecipe )

    client = get_client()
    client.load(image)
   
    # Add recipe parsers
    client.DockerRecipe = DockerRecipe
    client.SingularityRecipe = SingularityRecipe

    bpython.embed(locals_={'client': client})

def python(image):
    import code
    from spython.main import get_client
    from spython.main.parse import ( DockerRecipe, SingularityRecipe )

    client = get_client()
    client.load(image)

    # Add recipe parsers
    client.DockerRecipe = DockerRecipe
    client.SingularityRecipe = SingularityRecipe

    code.interact(local={"client":client})
