
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


import hashlib
import os
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
        return image.strip('-').rstrip('/')


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


class Image(ImageBase):

    def __init__(self, image=None):
       '''An image here is an image file or a record.
          The user can choose to load the image when starting the client, or
          update the main client with an image. The image object is kept
          with the main client to make running additional commands easier.

          Parameters
          ==========
          image: the image uri to parse (required)

       '''
       super(ImageBase, self).__init__()
       self.parse_image_name(image)


    def get_hash(self, image=None):
        '''return an md5 hash of the file based on a criteria level. This
           is intended to give the file a reasonable version. This only is
           useful for actual image files.
    
           Parameters
           ==========
           image: the image path to get hash for (first priority). Second
                  priority is image path saved with image object, if exists.

        '''
        hasher = hashlib.md5()
        image = image or self.image
 
        if os.path.exists(image):
            with open(image, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
                return hasher.hexdigest()

        bot.warning('%s does not exist.' %image)
