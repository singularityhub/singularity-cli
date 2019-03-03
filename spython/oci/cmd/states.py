
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
import json


def state(self, container_id=None, sudo=False, sync_socket=False):

    ''' get the state of an OciImage, if it exists. The optional states that
        can be returned are created, running, stopped or (not existing).

        Equivalent command line example:      
           singularity oci state <container_ID>
          
        Parameters
        ==========
        container_id: the id to get the state of.
        sudo: Add sudo to the command. If the container was created by root,
              you need sudo to interact and get its state.
        sync_socket: the path to the unix socket for state synchronization

        Returns
        =======
        state: a parsed json of the container state, if exists. If the
               container is not found, None is returned.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci state
    cmd = self._init_command('state')

    if sync_socket != None:
        cmd = cmd + ['--sync-socket', sync_socket]

    # Finally, add the container_id
    cmd.append(container_id)

    # Generate the instance
    result = self._run_command(cmd, sudo=sudo, quiet=True)

    # Return the state object to the user
    if result['return_code'] == 0:
        return json.loads(result['message'][0])
    

def start(self, container_id=None, sudo=False):

    ''' start a previously invoked OciImage, if it exists.

        Equivalent command line example:      
           singularity oci start <container_ID>
           
        Parameters
        ==========
        container_id: the id to start.
        sudo: Add sudo to the command. If the container was created by root,
              you need sudo to interact and get its state.

        Returns
        =======
        return_code: the return code to indicate if the container was started.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci state
    cmd = self._init_command('start')

    # Finally, add the container_id
    cmd.append(container_id)

    # Run the command, return return code
    return self._run_and_return(cmd, sudo)


def kill(self, container_id=None, sudo=False):

    ''' stop (kill) a started OciImage container, if it exists

        Equivalent command line example:      
           singularity oci kill <container_ID>
           
        Parameters
        ==========
        container_id: the id to stop.
        sudo: Add sudo to the command. If the container was created by root,
              you need sudo to interact and get its state.

        Returns
        =======
        return_code: the return code to indicate if the container was killed.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci state
    cmd = self._init_command('kill')

    # Finally, add the container_id
    cmd.append(container_id)

    # Run the command, return return code
    return self._run_and_return(cmd, sudo)


def resume(self, container_id=None, sudo=False):
    ''' resume a stopped OciImage container, if it exists

        Equivalent command line example:      
           singularity oci resume <container_ID>
           
        Parameters
        ==========
        container_id: the id to stop.
        sudo: Add sudo to the command. If the container was created by root,
              you need sudo to interact and get its state.

        Returns
        =======
        return_code: the return code to indicate if the container was resumed.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci state
    cmd = self._init_command('resume')

    # Finally, add the container_id
    cmd.append(container_id)

    # Run the command, return return code
    return self._run_and_return(cmd, sudo)
