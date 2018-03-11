# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.
# Copyright (C) 2016-2018 Vanessa Sochat.

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

# These parsing functions are specific to environment lines, used across recipes

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

    # This will need a lot of love!
    # Detail work not yet done here, see link above for possible cases

    for env in envlist:

        pieces = re.split("( |\\\".*?\\\"|'.*?')", env)
        pieces = [p for p in pieces if p.strip()]
        export = "=".join(pieces)
        exports.append(export)

    return exports
