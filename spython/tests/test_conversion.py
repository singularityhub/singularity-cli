#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
import unittest
import tempfile
import shutil
import filecmp
from glob import glob
import os

print("########################################################test_conversion")

class TestConversion(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.d2s = os.path.join(self.pwd, 'tests', 'testdata', 'docker2singularity')
        self.s2d = os.path.join(self.pwd, 'tests', 'testdata', 'singularity2docker')
        self.tmpdir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_pairs(self):

        print('Testing that each recipe file has a pair of the other type.')
        dockerfiles = glob(os.path.join(self.d2s, '*.docker'))
        dockerfiles += glob(os.path.join(self.s2d, '*.docker'))

        for dockerfile in dockerfiles:
            name, _ = os.path.splitext(dockerfile)
            recipe = "%s.def" % name

            if not os.path.exists(recipe):
                print('%s does not exist.' % recipe)
            self.assertTrue(os.path.exists(recipe))


    def test_docker2singularity(self):

        print('Testing spython conversion from docker2singularity')
        from spython.main.parse.parsers import DockerParser
        from spython.main.parse.writers import SingularityWriter
 
        dockerfiles = glob(os.path.join(self.d2s, '*.docker'))

        for dockerfile in dockerfiles:
            name, _ = os.path.splitext(dockerfile)

            # Matching Singularity recipe ends with name
            recipe = "%s.def" % name

            parser = DockerParser(dockerfile)
            writer = SingularityWriter(parser.recipe)

            suffix = next(tempfile._get_candidate_names())
            output_file = "%s.%s" %(os.path.join(self.tmpdir, 
                                    os.path.basename(recipe)), suffix)

            # Write generated content to file
            with open(output_file, 'w') as filey:
                filey.write(writer.convert())

            # Compare to actual
            if not filecmp.cmp(recipe, output_file):
                print('Comparison %s to %s failed.' %(recipe, output_file))
            self.assertTrue(filecmp.cmp(recipe, output_file))

    def test_singularity2docker(self):

        print('Testing spython conversion from singularity2docker')
        from spython.main.parse.parsers import SingularityParser
        from spython.main.parse.writers import DockerWriter
 
        recipes = glob(os.path.join(self.s2d, '*.def'))

        for recipe in recipes:
            name, _ = os.path.splitext(recipe)
            dockerfile = "%s.docker" % name

            parser = SingularityParser(recipe)
            writer = DockerWriter(parser.recipe)

            suffix = next(tempfile._get_candidate_names())
            output_file = "%s.%s" %(os.path.join(self.tmpdir, 
                                    os.path.basename(dockerfile)), suffix)

            # Write generated content to file
            with open(output_file, 'w') as filey:
                filey.write(writer.convert())

            # Compare to actual
            if not filecmp.cmp(dockerfile, output_file):
                print('Comparison %s to %s failed.' %(dockerfile, output_file))
            self.assertTrue(filecmp.cmp(dockerfile, output_file))
            

if __name__ == '__main__':
    unittest.main()
