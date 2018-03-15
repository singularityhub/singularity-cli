
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


import sys

def main(args, options, parser):
    '''This function serves as a wrapper around the DockerRecipe and
       SingularityRecipe converters. We can either save to file if
       args.outfile is defined, or print to the console if not.
    '''

    from spython.main.parse import ( DockerRecipe, SingularityRecipe )

    # We need something to work with
    if not args.files:
        parser.print_help()
        sys.exit(1)

    # Get the user specified input and output files
    outfile = None    
    if len(args.files) > 1:
        outfile = args.files[1]

    # Choose the recipe parser
    parser = SingularityRecipe
    if args.input == "docker":
        parser = DockerRecipe
    elif args.input == "singularity":
        parser = SingularityRecipe(args.files[0])
    else:
        if "dockerfile" in args.files[0].lower():
            parser = DockerRecipe

    # Initialize the chosen parser
    parser = parser(args.files[0])

    # By default, discover entrypoint / cmd from Dockerfile
    entrypoint = "/bin/bash"
    force = False

    if args.entrypoint is not None:
        entrypoint = args.entrypoint
        force = True

    # If the user specifies an output file, save to it
    if outfile is not None:
        parser.save(outfile, runscript=entrypoint, force=force)

    # Otherwise, convert and print to screen
    else:
        recipe = parser.convert(runscript=entrypoint, force=True)
        print(recipe)
