'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

def get_client(quiet=False):
    '''
       get the client and perform imports not on init, in case there are any
       initialization or import errors. 

       Parameters
       ==========
       quiet: if True, suppress most output about the client

    '''
    from client import Client

    Client.quiet = quiet

    # Do imports here, can be customized
    from .apps import apps
    from .bootstrap import bootstrap
    from .build import build
    from .execute import execute 
    from .help import help
    from .inspect import inspect
    from .pull import pull

    # Actions
    Client.apps = apps
    Client.bootstrap = bootstrap
    Client.build = build
    Client.execute = execute
    Client.help = help
    Client.inspect = inspect
    Client.pull = pull

    # Command Grooups
    from .image import image_group
    Client.image = image_group

    # Initialize
    cli = Client()
    return cli

Singularity = get_client()
