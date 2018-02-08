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

    def create(self,image_path,size=None,sudo=False):
        '''create will create a a new image
        :param image_path: full path to image
        :param size: image sizein MiB, default is 1024MiB
        :param filesystem: supported file systems ext3/ext4 (ext[2/3]: default ext3
        '''        
        if size == None:
            size=1024

        if self.debug == True:
            cmd = ['singularity','--debug','image.create','--size',str(size),image_path]
        else:
            cmd = ['singularity','image.create','--size',str(size),image_path]
        output = self.run_command(cmd,sudo=sudo)
        self.println(output)

        if not os.path.exists(image_path):
            bot.error("Could not create image %s" %image_path)
            sys.exit(1)

        return image_path


