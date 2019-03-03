
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.image import ImageBase
import os

class OciImage(ImageBase):

    def __init__(self, container_id, bundle=None, create=True):
        ''' An Oci Image is an Image Base with OCI functions appended

            Parameters
            ==========
            container_id: image uri to parse (required)
            bundle: a bundle directory to create a container from.
                    the bundle should have a config.json at the root
            create: if the bundle is provided, create a container (default True)
        '''
        super(ImageBase, self).__init__()
        self.parse_container_id(container_id)

        self.options = []
        self.cmd = []

        # If bundle is provided, create it
        if bundle != None and create:
            self.bundle = bundle
            self.create(bundle, container_id, **kwargs)

# Unique resource identifier

    def get_container_id(self, container_id=None):
        ''' a helper function shared between functions that will return a 
            container_id. First preference goes to a container_id provided by
            the user at runtime. Second preference goes to the container_id
            instantiated with the client.

            Parameters
            ==========
            container_id: image uri to parse (required)
        '''

        # The user must provide a container_id, or have one with the client
        if container_id == None and self.container_id == None:
            bot.exit('You must provide a container_id.')

        # Choose whichever is not None, with preference for function provided
        container_id = container_id or self.container_id
        return container_id


    def parse_container_id(self, container_id):
        '''
            simply split the uri from the image. Singularity handles
            parsing of registry, namespace, image.
            
            Parameters
            ==========
            container_id: the complete container_id to create

        '''
        self.container_id = container_id
        self.uri = 'oci://'


    def get_uri(self):
        '''return the image uri (oci://) along with it's name
        '''
        return self.__str__()

# Naming

    def __str__(self):
        if hasattr(self, 'uri'):
            if self.uri:
                return "%s%s" %(self.uri, self.name)
        return os.path.basename(self.container_id)

    def __repr__(self):
        return self.__str__()


# Commands

    def _run_and_return(self, cmd, sudo=False):
        ''' Run a command, show the message to the user if quiet isn't set,
            and return the return code. This is a wrapper for the OCI client
            to run a command and easily return the return code value (what
            the user is ultimately interested in).

            Parameters
            ==========
            cmd: the command (list) to run.
            sudo: whether to add sudo or not.         

        '''

        result = self._run_command(cmd, sudo=sudo, quiet=True)

        # Show the response to the user, only if not quiet.
        if not self.quiet:
            bot.print(started['message'][0])

        # Return the state object to the user
        return result['return_code']


    def _init_command(self, action, flags=None):
        ''' a wrapper to the base init_command, ensuring that "oci" is added
            to each command

            Parameters
            ==========
            action: the main action to perform (e.g., build)
            flags: one or more additional flags (e.g, volumes) 
                   not implemented yet.

        '''
        from spython.main.base.command import init_command
        if not isinstance(action, list):
            action = [action]      
        cmd = ['oci'] + action
        return init_command(action, flags)
