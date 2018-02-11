#!/usr/bin/env python

'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from random import Random

class RobotNamer:

    _adjectives = [
        'chunky', 'buttery', 'delicious', 'scruptious', 'dinosaur', 'boopy',
        'lovely', 'carniverous', 'hanky', 'loopy', 'doopy', 'astute'
    ]

    _nouns = [
        'squidward', 'hippo', 'butter', 'animal', 'peas', 'lettuce', 'carrot',
        'onion', 'peanut', 'cupcake', 'muffin', 'buttface'
    ]

    def __init__(self):
        ''' set a random seed for choosing the name parts
        '''
        self.random = Random()


    def generate(self, delim='-', length=4, chars='0123456789'):
        '''
        Generate a robot name. Inspiration from Haikunator, but much more
                 poorly implemented ;)

        Parameters
        ==========
        delim: Delimiter
        length: TokenLength
        chars: TokenChars
        '''

        adjective = self._select(self._adjectives)
        noun = self._select(self._nouns)
        numbers = ''.join((self._select(chars) for _ in range(length)))
        return delim.join([adjective, noun, numbers])

    def _select(self, select_from):
        ''' select an element from a list using random.choice
        
            Parameters
            ==========
            should be a list of things to select from
        '''
        if len(select_from) <= 0:
            return ''

        return self.random.choice(select_from)


def main():
    bot = RobotNamer()
    print(bot.generate())

if __name__ == '__main__':
    main()
