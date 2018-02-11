
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



def parse_verbosity(self, args):
    '''parse_verbosity will take an argument object, and return the args
       passed (from a dictionary) to a list

       Parameters
       ==========
       args: the argparse argument objects

    '''

    flags = []

    if args.silent is True:
       flags.append('--silent')
    elif args.quiet is True:
        flags.append('--quiet')
    elif args.debug is True:
       flags.append('--debug')
    elif args.verbose is True:
       flags.append('-' + 'v' * args.verbose)

    return flags


'''
GLOBAL OPTIONS:
    -d|--debug    Print debugging information
    -h|--help     Display usage summary
    -s|--silent   Only print errors
    -q|--quiet    Suppress all normal output
       --version  Show application version
    -v|--verbose  Increase verbosity +1
    -x|--sh-debug Print shell wrapper debugging information

GENERAL COMMANDS:
    help       Show additional help for a command or container                  
    selftest   Run some self tests for singularity install                      

CONTAINER USAGE COMMANDS:
    exec       Execute a command within container                               
    run        Launch a runscript within container                              
    shell      Run a Bourne shell within container                              
    test       Launch a testscript within container                             

CONTAINER MANAGEMENT COMMANDS:
    apps       List available apps within a container                           
    bootstrap  *Deprecated* use build instead                                   
    build      Build a new Singularity container                                
    check      Perform container lint checks                                    
    inspect    Display container's metadata                                     
    mount      Mount a Singularity container image                              
    pull       Pull a Singularity/Docker container to $PWD                      
    siflist    list data object descriptors of a SIF container image            
    sign       Sign a group of data objects in container                        
    verify     Verify the crypto signature of group of data objects in container

COMMAND GROUPS:
    capability User's capabilities management command group                     
    image      Container image command group                                    
    instance   Persistent instance command group                                

'''
