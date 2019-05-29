#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.utils import get_installdir
import unittest


print("########################################################### test_recipe")

class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        
    def test_recipe_base(self):

        print('Testing spython.main.parse.base Recipe')
        from spython.main.parse.recipe import Recipe
        recipe = Recipe()
        self.assertEqual(str(recipe), '[spython-recipe]')

        attributes = ['cmd', 'comments', 'entrypoint', 'environ', 'files',
                      'install', 'labels', 'ports', 'source', 'test',
                      'volumes', 'workdir']
 
        for att in attributes:
            self.assertTrue(hasattr(recipe, att))

if __name__ == '__main__':
    unittest.main()
