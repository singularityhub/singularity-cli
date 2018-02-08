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



    def inspect(self,image_path, json=True, quiet=False, app=None):

        '''inspect will show labels, defile, runscript, and tests for an image
        :param image_path: path of image to inspect
        :param json: print json instead of raw text (default True)
        :param app: if defined, return help in context of an app
        '''

        cmd = ['singularity','--quiet','inspect']

        if app is not None:
            cmd = cmd + ['--app', app]

        options = ['e','d','l','r','hf','t']
        [cmd.append('-%s' % x) for x in options]

        if json is True:
            cmd.append('--json')

        cmd.append(image_path)
        output = self.run_command(cmd)
        self.println(output,quiet=quiet)    
        return output
