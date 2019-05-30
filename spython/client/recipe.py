
# Copyright (C) 2017-2018 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.utils import write_file
import sys

def main(args, options, parser):
    '''This function serves as a wrapper around the DockerParser, 
       SingularityParser, DockerWriter, and SingularityParser converters. 
       We can either save to file if args.outfile is defined, or print 
       to the console if not.
    '''

    from spython.main.parse import parsers
    from spython.main.parse import writers

    # We need something to work with
    if not args.files:
        parser.print_help()
        sys.exit(1)

    # Get the user specified input and output files
    outfile = None    
    if len(args.files) > 1:
        outfile = args.files[1]

    # Choose the recipe parser
    parser = parsers.SingularityParser
    writer = writers.SingularityWriter
    if args.input == "docker":
        parser = parsers.DockerParser
        writer = writers.DockerWriter
    elif args.input == "singularity":
        parser = parsers.SingularityParser
        writer = writers.SingularityWriter        
    else:
        if "dockerfile" in args.files[0].lower():
            parser = parsers.DockerParser
            writer = writers.DockerWriter

    # Initialize the chosen parser
    recipeParser = parser(args.files[0])

    # By default, discover entrypoint / cmd from Dockerfile
    entrypoint = "/bin/bash"
    force = False

    if args.entrypoint is not None:
        entrypoint = args.entrypoint
        force = True

    # Do the conversion
    recipeWriter = writer(recipeParser.recipe)
    result = recipeWriter.convert(runscript=entrypoint, force=force)

    # If the user specifies an output file, save to it
    if outfile is not None:
        write_file(outfile, result)

    # Otherwise, convert and print to screen
    else:
        print(result)
