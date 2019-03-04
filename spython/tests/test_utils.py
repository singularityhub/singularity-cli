#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
import unittest
import tempfile
import shutil
import json
import os

print("############################################################ test_utils")

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        

    def test_write_read_files(self):
        '''test_write_read_files will test the functions write_file and read_file
        '''
        print("Testing utils.write_file...")
        from spython.utils import write_file
        import json
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_file(tmpfile,"hello!")
        self.assertTrue(os.path.exists(tmpfile))        

        print("Testing utils.read_file...")
        from spython.utils import read_file
        content = read_file(tmpfile)[0]
        self.assertEqual("hello!",content)

        from spython.utils import write_json
        print("Testing utils.write_json...")
        print("...Case 1: Providing bad json")
        bad_json = {"Wakkawakkawakka'}":[{True},"2",3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)        
        with self.assertRaises(TypeError) as cm:
            write_json(bad_json,tmpfile)

        print("...Case 2: Providing good json")        
        good_json = {"Wakkawakkawakka":[True,"2",3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_json(good_json,tmpfile)
        with open(tmpfile,'r') as filey:
            content = json.loads(filey.read())
        self.assertTrue(isinstance(content,dict))
        self.assertTrue("Wakkawakkawakka" in content)


    def test_check_install(self):
        '''check install is used to check if a particular software is installed.
        If no command is provided, singularity is assumed to be the test case'''
        print("Testing utils.check_install")
        from spython.utils import check_install
        is_installed = check_install()
        self.assertTrue(is_installed)
        is_not_installed = check_install('fakesoftwarename')
        self.assertTrue(not is_not_installed)


    def test_check_get_singularity_version(self):
        '''check that the singularity version is found to be that installed'''
        print("Testing utils.get_singularity_version")
        from spython.utils import get_singularity_version
        version = get_singularity_version()
        self.assertTrue(version != "")
        os.environ['SPYTHON_SINGULARITY_VERSION'] = "3.0"
        version = get_singularity_version()
        self.assertTrue(version == "3.0")


    def test_get_installdir(self):
        '''get install directory should return the base of where singularity
        is installed
        '''
        print("Testing utils.get_installdir")
        from spython.utils import get_installdir
        whereami = get_installdir()
        print(whereami)
        self.assertTrue(whereami.endswith('spython'))


    def test_remove_uri(self):
        print("Testing utils.remove_uri")
        from spython.utils import remove_uri
        self.assertEqual(remove_uri('docker://ubuntu'),'ubuntu')
        self.assertEqual(remove_uri('shub://vanessa/singularity-images'),'vanessa/singularity-images')



if __name__ == '__main__':
    unittest.main()
