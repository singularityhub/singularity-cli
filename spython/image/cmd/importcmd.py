# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


def importcmd(self, image_path, input_source):
    """import will import (stdin) to the image

       Parameters
       ==========
       image_path: path to image to import to. 
       input_source: input source or file
       import_type: if not specified, imports whatever function is given
       
    """
    from spython.utils import check_install

    check_install()

    cmd = ["singularity", "image.import", image_path, input_source]
    output = self.run_command(cmd, sudo=False)
    self.println(output)
    return image_path
