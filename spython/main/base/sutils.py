
# Singularity Image utils for interacting with the Image/Instance 
#           classes from the client


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
import os
import re

def load(self, image=None):
    '''load an image, either an actual path on the filesystem or a uri.

       Parameters
       ==========
       image: the image path or uri to load (e.g., docker://ubuntu 

    '''
    from spython.image import Image
    from spython.instance import Instance

    self.simage = Image(image)

    if image is not None:
        if image.startswith('instance://'):
            self.simage = Instance(image)
        bot.info(self.simage)


def setenv(self, variable, value):
    '''set an environment variable for Singularity
    
       Parameters
       ==========
       variable: the variable to set
       value: the value to set
    '''
    os.environ[variable] = value
    os.putenv(variable, value)
    bot.debug('%s set to %s' % (variable, value))


def get_filename(self, image=None, ext='simg'):
    '''return an image filename based on the image uri. If an image uri is
       not specified, we look for the loaded image.
 
       Parameters
       ==========
       image: the uri to base off of
       ext: the extension to use
    '''
    return "%s.%s" %(re.sub('^.*://','',image).replace('/','-'), ext)
    


def get_uri(self):
    ''' check if the loaded image object (self.simage) has an associated uri
        return if yes, None if not.
    '''
    if hasattr(self, 'simage'):
        if self.simage is not None:
            if self.simage.image not in ['', None]:
                # Concatenates the <uri>://<image>
                return str(self.simage)
