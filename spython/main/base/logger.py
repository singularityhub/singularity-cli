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


import os

def init_level(self, quiet=False):
    '''set the logging level based on the environment
        
       Parameters
       ==========
       quiet: boolean if True, set to quiet. Gets overriden by environment
              setting, and only exists to define default

    '''
        
    if os.environ.get('MESSAGELEVEL') == "QUIET":
        quiet = True

    self.quiet = quiet



def println(self, output, quiet=False):
    '''print will print the output, given that quiet is not True. This
       function also serves to convert output in bytes to utf-8

       Parameters
       ==========
       output: the string to print
       quiet: a runtime variable to over-ride the default.

    '''
    if isinstance(output,bytes):
        output = output.decode('utf-8')
    if self.quiet is False and quiet is False:
        print(output)
