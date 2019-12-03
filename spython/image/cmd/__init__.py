# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


def generate_image_commands():
    """ The Image client holds the Singularity image command group, mainly
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

    """

    class ImageClient(object):
        group = "image"

    from spython.main.base.logger import println
    from spython.main.base.command import init_command, run_command
    from .utils import compress, decompress
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
