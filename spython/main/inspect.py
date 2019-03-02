
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from spython.logger import bot
from spython.utils import ( 
    check_install, 
    get_singularity_version, 
    run_command
)

def inspect(self, image=None, json=True, app=None, quiet=True):
    '''inspect will show labels, defile, runscript, and tests for an image
    
       Parameters
       ==========
       image: path of image to inspect
       json: print json instead of raw text (default True)
       quiet: Don't print result to the screen (default True)
       app: if defined, return help in context of an app

    '''
    check_install()

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    cmd = self._init_command('inspect')
    if app is not None:
        cmd = cmd + ['--app', app]

    options = ['e','d','l','r','hf','t']

    # After Singularity 3.0, helpfile was changed to H from

    if "version 3" in get_singularity_version():
        options = ['e','d','l','r','H','t']

    [cmd.append('-%s' % x) for x in options]

    if json is True:
        cmd.append('--json')

    cmd.append(image)
    result = run_command(cmd, quiet=True)

    if result['return_code'] == 0:
        result = json.loads(result['message'][0])

        # If labels included, try parsing to json

        if 'labels' in result['attributes']:
            labels = json.loads(result['attributes']['labels'])
            result['attributes']['labels'] = labels

        if not quiet:
            print(json.dumps(result, indent=4))

    return result
