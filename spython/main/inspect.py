
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
