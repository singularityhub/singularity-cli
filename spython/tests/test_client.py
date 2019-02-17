#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

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


print("########################################################### test_client")

class TestClient(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.cli = Client
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_commands(self):

        print('Testing client.build command')
        container = "%s/container.img" %(self.tmpdir)

        print("...Case 1: Build from docker uri")
        created_container = self.cli.build('docker://ubuntu', 
                                           image=container,
                                           sudo=False)
        self.assertEqual(created_container, container)
        self.assertTrue(os.path.exists(created_container))
        os.remove(container)

        print("Testing client.pull command")
        print("...Case 1: Testing naming pull by image name")
        image = self.cli.pull("shub://vsoch/singularity-images", 
                              pull_folder=self.tmpdir)
        self.assertTrue(os.path.exists(image))
        self.assertTrue('vsoch-singularity-images' in image)
        print(image)

        print('Testing client.run command')
        result = self.cli.run(image)
        print(result)
        self.assertTrue('You say please, but all I see is pizza..' in result)
        os.remove(image)

        print("...Case 2: Testing docker pull")
        container = self.cli.pull("docker://ubuntu:14.04",
                                   pull_folder=self.tmpdir)
        self.assertTrue("ubuntu:14.04" in container)

        print(container)
        self.assertTrue(os.path.exists(container))

        print('Testing client.execute command')
        result = self.cli.execute(container,'ls /')
        print(result)
        self.assertTrue('bin\nboot\ndev' in result)

        print("Testing client.inspect command")
        result = self.cli.inspect(container)
        labels = json.loads(result)
        self.assertTrue('data' in labels)     
        os.remove(container)



if __name__ == '__main__':
    unittest.main()
