'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from spython.logger import bot

def apps(self,image_path, full_path=False):
    '''
       return list of SCIF apps in image. The Singularity software serves
       a scientific filesystem integration that will install apps to
       /scif/apps and associated data to /scif/data. For more information 
       about SCIF, see https://sci-f.github.io

       Parameters
       ==========
       full_path: if True, return relative to scif base folder
       image_path: full path to the image

    '''
    cmd = ['singularity','apps',image_path]
    output = self.run_command(cmd)

    if output not in ['', None]:   

        self.println(output)
        output = output.strip().split('\n')

        if full_path is True:
            output = ['/scif/apps/%s' %x for x in output]
        return output
