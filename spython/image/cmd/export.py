# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
import tempfile


def export(self, image_path, tmptar=None):
    """export will export an image, sudo must be used.

       Parameters
       ==========
   
       image_path: full path to image
       tmptar: if defined, use custom temporary path for tar export

    """
    from spython.utils import check_install

    check_install()

    if "version 3" in self.version():
        bot.exit("export is deprecated after Singularity 2.*")

    if tmptar is None:
        tmptar = "/%s/tmptar.tar" % (tempfile.mkdtemp())
    cmd = ["singularity", "image.export", "-f", tmptar, image_path]

    self.run_command(cmd, sudo=False)
    return tmptar
