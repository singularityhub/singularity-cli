
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
import tempfile

def export(self, image_path, tmptar=None):
    '''export will export an image, sudo must be used.

       Parameters
       ==========
   
       image_path: full path to image
       tmptar: if defined, use custom temporary path for tar export

    '''
    from spython.utils import check_install
    check_install()

    if tmptar is None:
        tmptar = "/%s/tmptar.tar" %(tempfile.mkdtemp())
    cmd = ['singularity', 'image.export', '-f', tmptar, image_path]

    output = self.run_command(cmd, sudo=False)
    return tmptar
