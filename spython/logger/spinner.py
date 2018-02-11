
# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.
# Copyright (C) 2017-2018 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys

import sys
import time
import threading
from random import choice

class Spinner:
    spinning = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    @staticmethod
    def balloons_cursor():
        while 1: 
            for cursor in '. o O @ *': yield cursor

    @staticmethod
    def changing_arrows():
        while 1: 
            for cursor in '<^>v': yield cursor

    def select_generator(self, generator):
        if generator == None:
            generator = choice(['cursor',
                                'arrow',
                                'balloons'])

        return generator

    def __init__(self, delay=None, generator=None):
        generator = self.select_generator(generator)

        if generator == 'cursor':
            self.spinner_generator = self.spinning_cursor()
        elif generator == 'arrow':
            self.spinner_generator = self.changing_arrows()
        elif generator == 'balloons':
            self.spinner_generator = self.balloons_cursor()
            if delay is None: delay = 0.2
        else:
            self.spinner_generator = self.spinning_cursor()

        if delay and float(delay):
            self.delay = delay

    def run(self):
        while self.spinning:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.spinning = True
        threading.Thread(target=self.run).start()

    def stop(self):
        self.spinning = False
        time.sleep(self.delay)
