
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot

def stop(self, name=None, sudo=False):
    '''stop an instance. This is done by default when an instance is created.

       Parameters
       ==========
       name: a name for the instance
       sudo: if the user wants to run the command with sudo

       USAGE: 
       singularity [...] instance.stop [...] <instance name>

    '''        
    from spython.utils import (check_install, run_command)
    check_install()

    subgroup = 'instance.stop'

    if 'version 3' in self.version():
        subgroup = ["instance", "stop"]

    cmd = self._init_command(subgroup)

    # If name is provided assume referencing an instance
    instance_name = self.name
    if name is not None:
        instance_name = name     
    cmd = cmd + [instance_name]
    
    output = run_command(cmd, sudo=sudo, quiet=True)

    if output['return_code'] != 0:
        message = '%s : return code %s' %(output['message'], 
                                          output['return_code'])
        bot.error(message)
        return output['return_code']

    return output['return_code']
