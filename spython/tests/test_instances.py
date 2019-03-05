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


print("######################################################## test_instances")

class TestInstances(unittest.TestCase):

    def setUp(self):
        self.cli = Client
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_instances(self):

        print('Pulling testing container')
        image = self.cli.pull("docker://busybox:1.30.1", 
                              pull_folder=self.tmpdir)
        self.assertTrue(os.path.exists(image))
        self.assertTrue('busybox:1.30.1' in image)
        print(image)

        print("...Case 0: No instances: objects")
        instances = self.cli.instances()
        self.assertEqual(instances, [])
        
        print("...Case 1: Create instance")
        myinstance = self.cli.instance(image)
        self.assertTrue(myinstance.get_uri().startswith('instance://'))

        print("...Case 2: List instances")
        instances = self.cli.instances()
        self.assertEqual(len(instances), 1)
        instances = self.cli.instances(return_json=True)
        self.assertEqual(len(instances), 1)
        self.assertTrue(isinstance(instances[0], dict))

        print("...Case 3: Commands to instances")
        result = self.cli.execute(myinstance, ['echo', 'hello'])
        self.assertTrue('hello\n' == result)

        print('...Case 4: Return value from instance')
        result = self.cli.execute(myinstance,'ls /', return_result=True)
        print(result)
        self.assertTrue('tmp\nusr\nvar' in result['message'])
        self.assertEqual(result['return_code'], 0)

        print("...Case 5: Stop instances")
        myinstance.stop()
        instances = self.cli.instances()
        self.assertEqual(instances, [])
        myinstance1 = self.cli.instance(image)
        myinstance2 = self.cli.instance(image)
        instances = self.cli.instances()
        self.assertEqual(len(instances), 2)
        self.cli.instance_stopall()
        instances = self.cli.instances()
        self.assertEqual(instances, [])


if __name__ == '__main__':
    unittest.main()
