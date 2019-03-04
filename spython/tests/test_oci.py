#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
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
                                     container_id='mycontainer')

        print(result)
        self.assertEqual(result['status'], 'created')

        print('...Case 3. Check status of existing bundle.')
        state = self.cli.oci.state('mycontainer', sudo=True)
        self.assertEqual(result['status'], 'created')

        print('...Case 4. Start container.')
        state = self.cli.oci.start('mycontainer', sudo=True)
        self.assertEqual(state, None)

        print('...Case 5. Pause running container.')
        state = self.cli.oci.pause('mycontainer', sudo=True)
        self.assertEqual(state, None)

        print('...Case 6. Resume paused container.')
        state = self.cli.oci.resume('mycontainer', sudo=True)
        self.assertEqual(state, None)

        print('...Case 7. Kill should work with running container.')
        state = self.cli.oci.kill('mycontainer', sudo=True)
        self.assertEqual(state, None)

        print('...Case 8. Resume should not work with non running container.')
        state = self.cli.oci.resume('mycontainer', sudo=True)
        self.assertEqual(state, 255)

        # Clean up the image (should still use sudo)
        result = self.cli.oci.delete('mycontainer', sudo=True)
        self.assertEqual(result, None)

        # Try delete operation with opposite, should return 255
        result = self.cli.oci.delete('mycontainer', sudo=True)
        self.assertEqual(result, 255)


if __name__ == '__main__':
    unittest.main()
