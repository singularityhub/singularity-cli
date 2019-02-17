
# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re


def parse_env(envlist):
    '''parse_env will parse a single line (with prefix like ENV removed) to
    a list of commands in the format KEY=VALUE For example:

        ENV PYTHONBUFFER 1 --> [PYTHONBUFFER=1]

    ::Notes
      Docker: https://docs.docker.com/engine/reference/builder/#env

    '''
    if not isinstance(envlist, list):
        envlist = [envlist]

    exports = [] 

    for env in envlist:

        pieces = re.split("( |\\\".*?\\\"|'.*?')", env)
        pieces = [p for p in pieces if p.strip()]

        while len(pieces) > 0:

            current = pieces.pop(0)

            if current.endswith('='):

                # Case 1: ['A='] --> A=

                next = ""

                # Case 2: ['A=', '"1 2"'] --> A=1 2

                if len(pieces) > 0:
                    next = pieces.pop(0)
                exports.append("%s%s" %(current, next))

            # Case 2: ['A=B']     --> A=B

            elif '=' in current:
                exports.append(current)

            # Case 3: ENV \\

            elif current.endswith('\\'):
                continue

            # Case 4: ['A', 'B']  --> A=B

            else:

                next = pieces.pop(0)
                exports.append("%s=%s" %(current, next))

    return exports
