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
                      'install', 'labels', 'ports', 'test',
                      'volumes', 'workdir']
 
        for att in attributes:
            self.assertTrue(hasattr(recipe, att))

        print('Checking that empty recipe returns empty')
        result = recipe.json()
        self.assertTrue(not result)

        print('Checking that non-empty recipe returns values')
        recipe.cmd = ['echo', 'hello']
        recipe.entrypoint = '/bin/bash'
        recipe.comments = ['This recipe is great', 'Yes it is!']
        recipe.environ = ['PANCAKES=WITHSYRUP']
        recipe.files = [['one', 'two']]
        recipe.test = ['true']
        recipe.install = ['apt-get update']
        recipe.labels = ['Maintainer vanessasaur']
        recipe.ports = ['3031']
        recipe.volumes = ['/data']
        recipe.workdir = '/code'

        result = recipe.json()
        for att in attributes:
            self.assertTrue(att in result)

if __name__ == '__main__':
    unittest.main()
