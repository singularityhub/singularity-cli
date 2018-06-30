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


from spython.image import ImageBase
import os

class Instance(ImageBase):

    def __init__(self, image, start=True, **kwargs):
       '''An instance is an image running as an instance with services.
          This class has functions appended under cmd/__init__ and is
          instantiated when the user calls Client.

          Parameters
          ==========
          image: the Singularity image uri to parse (required)
          start: boolean to start the instance (default is True)

       '''
       super(ImageBase, self).__init__()
       self.parse_image_name(image)

       # Update metadats from arguments
       self._update_metadata(kwargs)
       self.options = []
       self.cmd = []

       # Start the instance
       if start is True:
           self._start(**kwargs)

# Unique resource identifier

    def parse_image_name(self, image):
        '''
            simply split the uri from the image. Singularity handles
            parsing of registry, namespace, image.
            
            Parameters
            ==========
            image: the complete image uri to load (e.g., docker://ubuntu) 

        '''
        self._image = image
        self.uri = 'instance://'


    def get_uri(self):
        '''return the image uri (instance://) along with it's name
        '''
        return self.__str__()

# Metadata

    def _update_metadata(self, kwargs=None):
        '''Extract any additional attributes to hold with the instance
           from kwargs
        '''

        # If not given metadata, use instance.list to get it for container
        if kwargs is None:
            kwargs = self._list(self.name, quiet=True, return_json=True)

        # Add acceptable arguments
        for arg in ['pid', 'name']:

           # Skip over non-iterables:
           if arg in kwargs:
               setattr(self, arg, kwargs[arg])
       
        if "image" in kwargs:
            self._image = kwargs['image']
        elif "container_image" in kwargs:
            self._image = kwargs['container_image']


    def __str__(self):
        if hasattr(self, 'uri'):
            if self.uri:
                return "%s%s" %(self.uri, self.name)
        return os.path.basename(self._image)

    def __repr__(self):
        return self.__str__()
