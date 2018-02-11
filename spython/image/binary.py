
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


from .base import ImageBase
import hashlib
import os

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
