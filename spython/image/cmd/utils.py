
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

def compress(self, image_path):
    '''compress will (properly) compress an image'''
    if os.path.exists(image_path):
        compressed_image = "%s.gz" %image_path
        os.system('gzip -c -6 %s > %s' %(image_path, compressed_image))
        return compressed_image

    bot.exit("Cannot find image %s" %image_path)


def decompress(self, image_path, quiet=True):
    '''decompress will (properly) decompress an image'''

    if not os.path.exists(image_path):
        bot.exit("Cannot find image %s" %image_path)
        
    extracted_file = image_path.replace('.gz','')
    cmd = ['gzip','-d','-f', image_path]
    result = self.run_command(cmd, quiet=quiet) # exits if return code != 0
    return extracted_file
