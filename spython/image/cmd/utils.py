# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
from spython.logger import bot


def compress(self, image_path):
    """compress will (properly) compress an image"""
    if os.path.exists(image_path):
        compressed_image = "%s.gz" % image_path
        os.system("gzip -c -6 %s > %s" % (image_path, compressed_image))
        return compressed_image

    bot.exit("Cannot find image %s" % image_path)


def decompress(self, image_path, quiet=True):
    """decompress will (properly) decompress an image"""

    if not os.path.exists(image_path):
        bot.exit("Cannot find image %s" % image_path)

    extracted_file = image_path.replace(".gz", "")
    cmd = ["gzip", "-d", "-f", image_path]
    self.run_command(cmd, quiet=quiet)  # exits if return code != 0
    return extracted_file
