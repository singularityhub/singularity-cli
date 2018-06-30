
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


def get_client(quiet=False, debug=False):
    '''
       get the client and perform imports not on init, in case there are any
       initialization or import errors. 

       Parameters
       ==========
       quiet: if True, suppress most output about the client
       debug: turn on debugging mode

    '''
    from .base import Client

    Client.quiet = quiet
    Client.debug = debug

    # Do imports here, can be customized
    from .apps import apps
    from .build import build
    from .execute import execute 
    from .help import help
    from .inspect import inspect
    from .instances import ( instances, stopall ) # global instance commands
    from .run import run
    from .pull import pull

    # Actions
    Client.apps = apps
    Client.build = build
    Client.execute = execute
    Client.help = help
    Client.inspect = inspect
    Client.instances = instances
    Client.run = run
    Client.pull = pull

    # Command Groups, Images
    from spython.image.cmd import image_group        # deprecated image commands
    Client.image = image_group

    # Commands Groups, Instances
    from spython.instance.cmd import instance_group  # instance level commands
    Client.instance = instance_group
    Client.instance_stopall = stopall

    # Initialize
    cli = Client()

    # Pass on verbosity
    cli.image.debug = cli.debug
    cli.image.quiet = cli.quiet
    cli.instance.debug = cli.debug
    cli.instance.quiet = cli.quiet

    return cli

Client = get_client()
