
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

def inspect(self,image=None, json=True, app=None):
    '''inspect will show labels, defile, runscript, and tests for an image
    

       Parameters
       ==========
       image_path: path of image to inspect
       json: print json instead of raw text (default True)
       app: if defined, return help in context of an app

    '''
    from spython.utils import check_install
    check_install()

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    cmd = self._init_command('inspect')
    if app is not None:
        cmd = cmd + ['--app', app]

    options = ['e','d','l','r','hf','t']
    [cmd.append('-%s' % x) for x in options]

    if json is True:
        cmd.append('--json')

    cmd.append(image)
    output = self._run_command(cmd)
    #self.println(output,quiet=self.quiet)    
    return output
