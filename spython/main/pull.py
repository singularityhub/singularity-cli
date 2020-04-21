# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
from spython.utils import stream_command, ScopedEnvVar
import os
import re


def pull(
    self,
    image=None,
    name=None,
    pull_folder="",
    ext=None,
    force=False,
    capture=False,
    stream=False,
    quiet=False,
    singularity_options=None,
):

    """pull will pull a singularity hub or Docker image
        
       Parameters
       ==========
       image: the complete image uri. If not provided, the client loaded is used
       singularity_options: a list of options to provide to the singularity client
       pull_folder: if not defined, pulls to $PWD (''). If defined, pulls to
                    user specified location instead.

       Docker and Singularity Hub Naming
       ---------------------------------
       name: a custom name to use, to override default
       ext: if no name specified, the default extension to use.

    """
    from spython.utils import check_install

    check_install()

    cmd = self._init_command("pull", singularity_options)

    # Quiet is honored if set by the client, or user
    quiet = quiet or self.quiet

    if not ext:
        ext = "sif" if "version 3" in self.version() else "simg"

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # If it's still None, no go!
    if image is None:
        bot.exit("You must provide an image uri, or use client.load() first.")

    # Singularity Only supports shub, docker and library pull
    if not re.search("^(shub|docker|library)://", image):
        bot.exit("pull only valid for docker, shub and library. Use sregistry client.")

    # If we still don't have a custom name, base off of image uri.
    if name is None:
        name = self._get_filename(image, ext)

    if pull_folder:
        final_image = os.path.join(pull_folder, os.path.basename(name))

        # Regression Singularity 3.* onward, PULLFOLDER not honored
        # https://github.com/sylabs/singularity/issues/2788
        if "version 3" in self.version():
            name = final_image
            pull_folder = None  # Don't use pull_folder
    else:
        final_image = name

    cmd = cmd + ["--name", name]

    if force:
        cmd = cmd + ["--force"]

    cmd.append(image)

    if not quiet:
        bot.info(" ".join(cmd))

    with ScopedEnvVar("SINGULARITY_PULLFOLDER", pull_folder):
        # Option 1: Streaming we just run to show user
        if not stream:
            self._run_command(cmd, capture=capture, quiet=quiet)

        # Option 3: A custom name we can predict (not commit/hash) and can also show
        else:
            return final_image, stream_command(cmd, sudo=False)

    if os.path.exists(final_image) and not quiet:
        bot.info(final_image)
    return final_image
