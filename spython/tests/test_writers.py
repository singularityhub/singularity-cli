#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
import unittest
import tempfile
import shutil
import os


print("########################################################## test_writers")

class TestWriters(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_docker_writer(self):

        print('Testing spython.main.parse.writers DockerWriter')
        from spython.main.parse.writers import DockerWriter
        from spython.main.parse.parsers import DockerParser

        dockerfile = os.path.join(self.pwd, 'tests', 'testdata', 'Dockerfile')        
        parser = DockerParser(dockerfile)
        writer = DockerWriter(parser.recipe)

        self.assertEqual(str(writer), '[spython-writer][docker]')
        print(writer.convert())


    def test_singularity_writer(self):

        print('Testing spython.main.parse.writers SingularityWriter')
        from spython.main.parse.writers import SingularityWriter
        from spython.main.parse.parsers import SingularityParser

        recipe = os.path.join(self.pwd, 'tests', 'testdata', 'Singularity')        
        parser = SingularityParser(recipe)
        writer = SingularityWriter(parser.recipe)

        self.assertEqual(str(writer), '[spython-writer][docker]')
        print(writer.convert())


if __name__ == '__main__':
    unittest.main()
