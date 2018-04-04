
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


import re

class ImageBase(object):

    def __str__(self):
        if hasattr(self, 'uri'):
            if self.uri:
                return "%s://%s" %(self.uri, self.image)
        return self.image


    def __repr__(self):
        return self.__str__()


    def get_uri(self, image):
        '''get the uri of an image, or the string (optional) that appears before
           ://. Optional. If none found, returns ''
        '''
        image = image or ''
        uri = ''

        match = re.match("^(?P<uri>.+)://", image)
        if match:
            uri = match.group('uri')

        return uri


    def remove_uri(self, image):
        '''remove_image_uri will return just the image name.
           this will also remove all spaces from the uri.
        '''
        image = image or ''
        uri = self.get_uri(image) or ''
        image = image.replace('%s://' %uri,'', 1)
        print(image)
        return image.strip('-').strip('/')

    def parse_image_name(self, image):
        '''
            simply split the uri from the image. Singularity handles
            parsing of registry, namespace, image.
            
            Parameters
            ==========
            image: the complete image uri to load (e.g., docker://ubuntu) 

        '''
        self._image = image
        self.uri = self.get_uri(image)
        self.image = self.remove_uri(image)
