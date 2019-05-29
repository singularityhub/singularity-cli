#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
from spython.main import Client
import unittest
import tempfile
import shutil
import os


print("########################################################### test_client")

class TestClient(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.cli = Client
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_docker_parser(self):

        print('Testing spython.main.parse.parsers DockerParser')
        from spython.main.parse.parsers import DockerParser

        dockerfile = os.path.join(self.pwd, 'tests', 'testdata', 'Dockerfile')        
        parser = DockerParser(dockerfile)

        self.assertEqual(str(parser), '[spython-parser][docker]')

        # Test all fields from recipe
        self.assertEqual(parser.recipe.fromHeader, 'python:3.5.1')
        self.assertEqual(parser.recipe.cmd, '/code/run_uwsgi.sh')
        self.assertEqual(parser.recipe.entrypoint, None)
        self.assertEqual(parser.recipe.workdir, '/code')
        self.assertEqual(parser.recipe.volumes, [])
        self.assertEqual(parser.recipe.ports, ['3031'])
        self.assertEqual(parser.recipe.files[0], ['requirements.txt', '/tmp/requirements.txt'])
        self.assertEqual(parser.recipe.environ, ['PYTHONUNBUFFERED=1'])
        self.assertEqual(parser.recipe.source, dockerfile)

    def test_singularity_parser(self):

        print('Testing spython.main.parse.parsers SingularityParser')
        from spython.main.parse.parsers import SingularityParser

        recipe = os.path.join(self.pwd, 'tests', 'testdata', 'Singularity')  
        parser = SingularityParser(recipe)

        self.assertEqual(str(parser), '[spython-parser][singularity]')

        # Test all fields from recipe
        self.assertEqual(parser.recipe.fromHeader, 'continuumio/miniconda3')
        self.assertEqual(parser.recipe.cmd, 'exec /opt/conda/bin/spython "$@"')
        self.assertEqual(parser.recipe.entrypoint, None)
        self.assertEqual(parser.recipe.workdir, None)
        self.assertEqual(parser.recipe.volumes, [])
        self.assertEqual(parser.recipe.ports, ['3031'])
        self.assertEqual(parser.recipe.files, [])
        self.assertEqual(parser.recipe.environ, [])
        self.assertEqual(parser.recipe.source, recipe)


if __name__ == '__main__':
    unittest.main()
