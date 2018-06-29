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


def generate_image_commands():
    ''' The Image client holds the Singularity image command group, mainly
        deprecated commands (image.import) and additional command helpers
        that are commonly use but not provided by Singularity

        The levels of verbosity (debug and quiet) are passed from the main
        client via the environment variable MESSAGELEVEL.

        These commands are added to Client.image under main/__init__.py to 
        expose subcommands:

            Client.image.export
            Client.image.imprt
            Client.image.decompress
            Client.image.create

    '''

    class ImageClient(object):
        group = "image"

    from spython.main.base.logger import println
    from spython.main.base.command import ( init_command, run_command )
    from .utils import ( compress, decompress )
    from .create import create
    from .importcmd import importcmd
    from .export import export

    ImageClient.create = create
    ImageClient.imprt = importcmd
    ImageClient.export = export
    ImageClient.decompress = decompress
    ImageClient.compress = compress
    ImageClient.println = println
    ImageClient.init_command = init_command
    ImageClient.run_command = run_command
 
    cli = ImageClient()
    return cli

image_group = generate_image_commands()
