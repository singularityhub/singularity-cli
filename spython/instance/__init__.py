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
       self.status = 'stopped'

       # Start the instance
       if start is True:
           self.start(**kwargs)

