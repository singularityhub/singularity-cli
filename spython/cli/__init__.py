#!/usr/bin/env python

'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

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

import argparse
import sys
import os


def get_parser():

    parser = argparse.ArgumentParser(description="Singularity Client",
                                formatter_class=argparse.RawTextHelpFormatter,
                                add_help=False)

    # Global Options
    parser.add_argument('--debug','-d', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--silent','-s', dest="silent", 
                        help="only print errors", 
                        default=False, action='store_true')


    parser.add_argument('--quiet','-q', dest="quiet", 
                        help="suppress all normal output", 
                        default=False, action='store_true')

    parser.add_argument('--version', dest="version", 
                        help="show singularity and spython version", 
                        default=False, action='store_true')

    parser.add_argument('--verbose','-v', action='count', 
                        help="add verbosity (-vvvv)") # args.verbose


    parser.add_argument('--sh-debug','-x', dest="shdebug", 
                        help="full shell wrapper debugging information", 
                        default=False, action='store_true')


    subparsers = parser.add_subparsers(help='description',
                                       title='actions',
                                       description='actions for Singularity',
                                       dest="command", metavar='general usage')

          
    # General Commands
    subparsers.add_parser("help", help="Show help for a command or container")
    subparsers.add_parser("selftest", help='''run self tests for singularity
                                      ''')

    # Container Usage Commands
    subparsers.add_parser("exec", help="Execute a command within container")
    subparsers.add_parser("pyshell", help="Interact with singularity python")
    subparsers.add_parser("run", help="Launch a runscript within container")                           
    subparsers.add_parser("shell", help="Run a Bourne shell within container")
    subparsers.add_parser("test", help='''Launch a testscript within container
                                    ''')

    # Container Management Commands
    subparsers.add_parser("apps", help="List available apps within a container")
    subparsers.add_parser("build", help="Build a new Singularity container")          
    subparsers.add_parser("check", help="Perform container lint checks")
    subparsers.add_parser("inspect", help="Display container's metadata")
    subparsers.add_parser("mount", help="Mount a Singularity container image")
    subparsers.add_parser("pull", help="Pull container to $PWD")
    subparsers.add_parser("siflist", help="list descriptors of a SIF image")
    subparsers.add_parser("sign", help="Sign a group of data objects in image")
    subparsers.add_parser("verify", help='''Verify signature of data objects
                                         ''')

    # Command groups (add as group?)
    subparsers.add_parser("capability", help="capabilities management command group")
    subparsers.add_parser("images", help="container image command group")
    subparsers.add_parser("instance", help="container instance command group")

    return parser



def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers


def set_verbosity(args):
    '''determine the message level in the environment to set based on args.
    '''
    level = "INFO"

    if args.debug is True:
        level = "DEBUG"
    elif args.verbose is not None:
        level = "VERBOSE%s" %args.verbose
    elif args.silent is True:
        level = "CRITICAL"
    elif args.quiet is True:
        level = "QUIET"

    os.environ['MESSAGELEVEL'] = level
    os.environ['SINGULARITY_MESSAGELEVEL'] = level
       
    # Import logger to set
    from spython.logger import bot
    bot.debug('Logging level %s' %level)
    import spython

    bot.info("Singularity Python Version: %s" % spython.__version__)

    
def main():

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''
        import spython
        version = spython.__version__

        print("\nSingularity Python [v%s]\n" %(version))
        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    #if len(sys.argv) == 1:
    #    help()
    #try:
        # We capture all primary arguments, and take secondary to pass on
    args, options = parser.parse_known_args()
    #except:
    #    sys.exit(0)

    # The main function
    main = None

    print("ARGS: %s" %args)
    print("OPTS: %s" %options)

    #TODO: --debug, --verbose, -vvv should be passed as options
    # need to figure out where they appear relative to cmd, and how to include
    # with other (cmd-specific options)
    #DEBUG = '--debug'
    #QUIET = '--quiet'
    #VERBOSE = '-vvvv'

    # Does the user want help for a subcommand?
    if args.command == 'help': from .help import main 

    elif args.command == 'apps': from .apps import main 
    elif args.command == 'build': from .build import main 
    elif args.command == 'caps': from .caps import main 
    elif args.command == 'check': from .check import main 
    elif args.command == 'exec': from .exec import main 
    elif args.command == 'images': from .images import main 
    elif args.command == 'inspect': from .inspect import main 
    elif args.command == 'instance': from .instance import main 
    elif args.command == 'mount': from .mount import main 
    elif args.command == 'pull': from .pull import main 
    elif args.command == 'pyshell': from .pyshell import main 
    elif args.command == 'run': from .run import main 
    elif args.command == 'selftest': from .selftest import main 
    elif args.command == 'shell': from .shell import main 
    elif args.command == 'siflist': from .siflist import main 
    elif args.command == 'sign': from .sign import main 
    elif args.command == 'test': from .test import main 
    elif args.command == 'verify': from .verify import main 

    wants_help = False
    if "help" or "--help" in options:
        wants_help = True

        # No command, show general help
        if main is None:
            help()
    
    # if environment logging variable not set, make silent
    set_verbosity(args)

    # Pass on to the correct parser
    if args.command is not None:
        main(args=args, options=options)


if __name__ == '__main__':
    main()
