
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.logger import bot
from spython.utils import stream_command


def run(self, bundle,
              container_id=None,
              log_path=None,
              pid_file=None,
              log_format="kubernetes"):

    ''' run is a wrapper to create, start, attach, and delete a container.

        Equivalent command line example:      
          singularity oci run -b ~/bundle mycontainer

        Parameters
        ==========
        bundle: the full path to the bundle folder
        container_id: an optional container_id. If not provided, use same
                      container_id used to generate OciImage instance
        log_path: the path to store the log.
        pid_file: specify the pid file path to use
    '''
    return self._run(self, bundle,
                     container_id=container_id,
                     empty_process=False,
                     log_path=log_path,
                     pid_file=pid_file,
                     sync_socket=None,
                     command="run",
                     log_format=log_format)


def create(self, bundle,
                 container_id=None,
                 empty_process=False,
                 log_path=None,
                 pid_file=None,
                 sync_socket=None,
                 log_format="kubernetes"): 

    ''' use the client to create a container from a bundle directory. The bundle
        directory should have a config.json. You must be the root user to
        create a runtime.

        Equivalent command line example:      
           singularity oci create [create options...] <container_ID>

        Parameters
        ==========
        bundle: the full path to the bundle folder
        container_id: an optional container_id. If not provided, use same
                      container_id used to generate OciImage instance
        empty_process: run container without executing container process (for
                       example, for a pod container)
        log_path: the path to store the log.
        pid_file: specify the pid file path to use
        sync_socket: the path to the unix socket for state synchronization.
    '''
    return self._run(self, bundle,
                     container_id=container_id,
                     empty_process=empty_process,
                     log_path=log_path,
                     pid_file=pid_file,
                     sync_socket=sync_socket,
                     command="create",
                     log_format=log_format)


def _run(self, bundle,
               container_id=None,
               empty_process=False,
               log_path=None,
               pid_file=None,
               sync_socket=None,
               command="run",
               log_format="kubernetes"): 

    ''' _run is the base function for run and create, the only difference
        between the two being that run does not have an option for sync_socket.

        Equivalent command line example:      
           singularity oci create [create options...] <container_ID>

        Parameters
        ==========
        bundle: the full path to the bundle folder
        container_id: an optional container_id. If not provided, use same
                      container_id used to generate OciImage instance
        empty_process: run container without executing container process (for
                       example, for a pod container)
        log_path: the path to store the log.
        pid_file: specify the pid file path to use
        sync_socket: the path to the unix socket for state synchronization.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci create
    cmd = self._init_command(command)

    # Check that the bundle exists
    if not os.path.exists(bundle):
        bot.exit('Bundle not found at %s' % bundle)

    # Add the bundle
    cmd = cmd + ['--bundle', bundle]

    # Additional Logging Files
    cmd = cmd + ['--log-format', log_format]

    if log_path != None:
        cmd = cmd + ['--log-path', log_path]
    if pid_file != None:
        cmd = cmd + ['--pid-file', pid_file]
    if sync_socket != None:
        cmd = cmd + ['--sync-socket', sync_socket]
    if empty_process:
        cmd.append('--empty-process')

    # Finally, add the container_id
    cmd.append(container_id)

    # Generate the instance
    result = self._send_command(cmd, sudo=True)

    # Get the status to report to the user!
    # TODO: Singularity seems to create even with error, can we check and
    # delete for the user if this happens?
    return self.oci.state(container_id, sudo, sync_socket)


def delete(self, container_id=None, sudo=False):
    '''delete an instance based on container_id.

       Parameters
       ==========
       container_id: the container_id to delete
       sudo: whether to issue the command with sudo (or not)
             a container started with sudo will belong to the root user
             If started by a user, the user needs to control deleting it

       Returns
       =======
       return_code: the return code from the delete command. 0 indicates a
                    successful delete, 255 indicates not.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('delete')

    # Add the container_id
    cmd.append(container_id)

    # Delete the container, return code goes to user (message to screen)
    return self._run_and_return(cmd, sudo)



def attach(self, container_id=None, sudo=False):
    '''attach to a container instance based on container_id

       Parameters
       ==========
       container_id: the container_id to delete
       sudo: whether to issue the command with sudo (or not)
             a container started with sudo will belong to the root user
             If started by a user, the user needs to control deleting it

       Returns
       =======
       return_code: the return code from the delete command. 0 indicates a
                    successful delete, 255 indicates not.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('attach')

    # Add the container_id
    cmd.append(container_id)

    # Delete the container, return code goes to user (message to screen)
    return self._run_and_return(cmd, sudo)


def execute(self, container_id=None, command=None, sudo=False):
    '''execute a command to a container instance based on container_id

       Parameters
       ==========
       container_id: the container_id to delete
       command: the command to execute to the container
       sudo: whether to issue the command with sudo (or not)
             a container started with sudo will belong to the root user
             If started by a user, the user needs to control deleting it

       Returns
       =======
       return_code: the return code from the delete command. 0 indicates a
                    successful delete, 255 indicates not.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('exec')

    if command != None:
        if not isinstance(command, list):
            command = [command]

        cmd = cmd + command

        # Add the container_id
        cmd.append(container_id)

        # Execute the command, return response to user
        return stream_command(cmd, sudo=sudo)


def update(self, container_id, from_file=None):
    '''update container cgroup resources for a specific container_id,
       The container must have state "running" or "created."

       Singularity Example:
           singularity oci update [update options...] <container_ID>
           singularity oci update --from-file cgroups-update.json mycontainer

       Parameters
       ==========
       container_id: the container_id to update cgroups for
       from_file: a path to an OCI JSON resource file to update from.
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('update')

    if from_file != None:
        cmd = cmd + ['--from-file', from_file]

    # Add the container_id
    cmd.append(container_id)

    # Delete the container, return code goes to user (message to screen)
    return self._run_and_return(cmd, sudo)
