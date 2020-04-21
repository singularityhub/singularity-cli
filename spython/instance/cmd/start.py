# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot


def start(
    self,
    image=None,
    name=None,
    args=None,
    sudo=False,
    options=None,
    capture=False,
    singularity_options=None,
):
    """start an instance. This is done by default when an instance is created.

       Parameters
       ==========
       image: optionally, an image uri (if called as a command from Client)
       name: a name for the instance
       sudo: if the user wants to run the command with sudo
       capture: capture output, default is False. With True likely to hang.
       args: arguments to provide to the instance (supported Singularity 3.1+)
       singularity_options: a list of options to provide to the singularity client
       options: a list of tuples, each an option to give to the start command
                [("--bind", "/tmp"),...]

       USAGE: 
       singularity [...] instance.start [...] <container path> <instance name>

    """
    from spython.utils import run_command, check_install

    check_install()

    # If name provided, over write robot (default)
    if name is not None:
        self.name = name

    # If an image isn't provided, we have an initialized instance
    if image is None:

        # Not having this means it was called as a command, without an image
        if not hasattr(self, "_image"):
            bot.exit("Please provide an image, or create an Instance first.")

        image = self._image

    # Derive subgroup command based on singularity version
    subgroup = "instance.start"
    if "version 3" in self.version():
        subgroup = ["instance", "start"]

    cmd = self._init_command(subgroup, singularity_options)

    # Add options, if they are provided
    if not isinstance(options, list):
        options = [] if options is None else options.split(" ")

    # Assemble the command!
    cmd = cmd + options + [image, self.name]

    # If arguments are provided
    if args is not None:
        if not isinstance(args, list):
            args = [args]
        cmd = cmd + args

    # Save the options and cmd, if the user wants to see them later
    self.options = options
    self.args = args
    self.cmd = cmd

    output = run_command(cmd, sudo=sudo, quiet=True, capture=capture)

    if output["return_code"] == 0:
        self._update_metadata()

    else:
        message = "%s : return code %s" % (output["message"], output["return_code"])
        bot.error(message)

    return self
