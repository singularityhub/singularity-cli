
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
from spython.utils import run_command, check_install

def instances(self, name=None, return_json=False, quiet=False):
    '''list instances. For Singularity, this is provided as a command sub
       group.

       singularity instance.list

       Return codes provided are different from standard linux:
       see https://github.com/singularityware/singularity/issues/1706

       Parameters
       ==========
       return_json: return a json list of instances instead of objects (False)
       name: if defined, return the list for just one instance (used to ged pid)

       Return Code  --   Reason
       0 -- Instances Found
       1 -- No Instances, libexecdir value not found, functions file not found
       255 -- Couldn't get UID

    '''
    from spython.instance.cmd.iutils import parse_table
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('instance.list')

    # If the user has provided a name, we want to see a particular instance
    if name is not None:
        cmd.append(name)

    output = run_command(cmd, quiet=True)
    instances = None

    # Success, we have instances

    if output['return_code'] == 0:

        # Only print the table if we are returning json
        if quiet is False:
            print(''.join(output['message']))

        # Prepare json result from table

        header = ['daemon_name','pid','container_image']
        instances = parse_table(output['message'][0], header)

        # Does the user want instance objects instead?
        listing = []
        if return_json is False:
            for i in instances:
                
                new_instance = self.instance(pid=i['pid'],
                                             name=i['daemon_name'],
                                             image=i['container_image'],
                                             start=False)

                listing.append(new_instance)
            instances = listing

    # Couldn't get UID

    elif output['return_code'] == 255:
        bot.error("Couldn't get UID")
        
    # Return code of 0
    else:
        bot.info('No instances found.')

    # If we are given a name, return just one
    if name is not None and instances is not None:
        if len(instances) == 1:
            instances = instances[0]

    return instances


def stopall(self, sudo=False, quiet=True):
    '''stop ALL instances. This command is only added to the command group
       as it doesn't make sense to call from a single instance

       Parameters
       ==========
       sudo: if the command should be done with sudo (exposes different set of
             instances)

    '''
    from spython.utils import run_command, check_install
    check_install()

    cmd = self._init_command('instance.stop')
    cmd = cmd + ['--all']
    output = run_command(cmd, sudo=sudo, quiet=quiet)

    if output['return_code'] != 0:
        message = '%s : return code %s' %(output['message'], 
                                          output['return_code'])
        bot.error(message)
        return output['return_code']

    return output['return_code']    
