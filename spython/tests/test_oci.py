#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
from spython.main.base.generate import RobotNamer
from spython.logger import bot
from spython.main import Client
import unittest
import tempfile
import shutil
import json
import os

print("############################################################## test_oci")

class TestOci(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.cli = Client
        self.tmpdir = tempfile.mkdtemp()
        shutil.rmtree(self.tmpdir) # bundle will be created here
        self.config = os.path.join(self.pwd, 'oci', 'config.json')
        self.name = RobotNamer().generate()

    def _build_sandbox(self):

        print('Building testing sandbox')
        image = self.cli.build("docker://busybox:1.30.1", 
                               image=self.tmpdir,
                               sandbox=True,
                               sudo=False)

        self.assertTrue(os.path.exists(image))

        print('Copying OCI config.json to sandbox...')
        shutil.copyfile(self.config, '%s/config.json' %image)
        return image

    def test_oci(self):

        image = self._build_sandbox()

        # A non existing process should not have a state
        print('...Case 1. Check status of non-existing bundle.')
        state = self.cli.oci.state('mycontainer')
        self.assertEqual(state, None)
        
        # This will use sudo
        print("...Case 2: Create OCI image from bundle")
        result = self.cli.oci.create(bundle=image,
                                     container_id=self.name)

        print(result)
        self.assertEqual(result['status'], 'created')

        print('...Case 3. Execute command to running bundle.')
        result = self.cli.oci.execute(container_id=self.name, 
                                      sudo=True, 
                                      command=['ls','/'])

        print(result)
        self.assertTrue('bin' in result)

        print('...Case 4. Check status of existing bundle.')
        state = self.cli.oci.state(self.name, sudo=True)
        self.assertEqual(state['status'], 'created')

        print('...Case 5. Start container return value 0.')
        state = self.cli.oci.start(self.name, sudo=True)
        self.assertEqual(state, 0)

        print('...Case 6. Testing that state is now running.')
        state = self.cli.oci.state(self.name, sudo=True)
        self.assertEqual(state['status'], 'running')

        print('...Case 7. Pause running container return value 0.')
        state = self.cli.oci.pause(self.name, sudo=True)
        self.assertEqual(state, 0)

        print('...Case 8. Resume paused container return value 0.')
        state = self.cli.oci.resume(self.name, sudo=True)
        self.assertEqual(state, 0)

        print('...Case 9. Kill container.')
        state = self.cli.oci.kill(self.name, sudo=True)
        self.assertEqual(state, 0)

        # Clean up the image (should still use sudo)
        # Bug in singularity that kill doesn't kill completely - this returns 
        # 255. When testsupdated to 3.1.* add signal=K to run
        result = self.cli.oci.delete(self.name, sudo=True)
        self.assertTrue(result in [0,255])


if __name__ == '__main__':
    unittest.main()
