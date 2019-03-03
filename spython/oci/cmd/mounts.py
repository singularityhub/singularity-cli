
# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
import sys


def mount(self, image):
    '''create an OCI bundle from SIF image

       Parameters
       ==========
       image: the container (sif) to mount
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('mount')

    # Add the container_id
    cmd.append(image)

    # return code goes to user (message to screen)
    return self._run_and_return(cmd, sudo)


def umount(self, image):
    '''delete an OCI bundle createdfrom SIF image

       Parameters
       ==========
       image: the container (sif) to mount
    '''
    container_id = self.get_container_id(container_id)

    # singularity oci delete
    cmd = self._init_command('umount')

    # Add the container_id
    cmd.append(image)

    # return code goes to user (message to screen)
    return self._run_and_return(cmd, sudo)
