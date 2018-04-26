
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


from spython.logger import bot

def importcmd(self, image_path, input_source):
    '''import will import (stdin) to the image

       Parameters
       ==========
       image_path: path to image to import to. 
       input_source: input source or file
       import_type: if not specified, imports whatever function is given
       
    '''
    from spython.utils import check_install
    check_install()

    cmd = ['singularity', 'image.import', image_path, input_source]
    output = self.run_command(cmd, sudo=False)
    self.println(output)        
    return image_path

