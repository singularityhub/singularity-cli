
# Copyright (C) 2017-2018 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
