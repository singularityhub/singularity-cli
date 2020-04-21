# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
from spython.logger import bot


def create(self, image_path, size=1024, sudo=False, singularity_options=None):
    """create will create a a new image

        Parameters
        ==========
        image_path: full path to image
        size: image sizein MiB, default is 1024MiB
        filesystem: supported file systems ext3/ext4 (ext[2/3]: default ext3
        singularity_options: a list of options to provide to the singularity client
    """
    from spython.utils import check_install

    check_install()

    cmd = self.init_command("image.create", singularity_options)
    cmd = cmd + ["--size", str(size), image_path]

    output = self.run_command(cmd, sudo=sudo)
    self.println(output)

    if not os.path.exists(image_path):
        bot.exit("Could not create image %s" % image_path)

    return image_path
