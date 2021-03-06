# Copyright (C) 2017-2021 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.utils import run_command as run_cmd

from spython.logger import bot

import subprocess
import sys
import os


def init_command(self, action, flags=None):
    """return the initial Singularity command with any added flags.

    Parameters
    ==========
    action: the main action to perform (e.g., build)
    flags: one or more additional singularity options
    """
    flags = flags or []

    if not isinstance(action, list):
        action = [action]
    cmd = ["singularity"] + flags + action

    if self.quiet:
        cmd.insert(1, "--quiet")
    if self.debug:
        cmd.insert(1, "--debug")

    return cmd


def generate_bind_list(self, bindlist=None):
    """generate bind string will take a single string or list of binds, and
     return a list that can be added to an exec or run command. For example,
     the following map as follows:

    ['/host:/container', '/both'] --> ["--bind", "/host:/container","--bind","/both" ]
    ['/both']                     --> ["--bind", "/both"]
    '/host:container'             --> ["--bind", "/host:container"]
     None                         --> []

     An empty bind or otherwise value of None should return an empty list.
     The binds are also checked on the host.

     Parameters
     ==========
     bindlist: a string or list of bind mounts

    """
    binds = []

    # Case 1: No binds provided
    if not bindlist:
        return binds

    # Case 2: provides a long string or non list, and must be split
    if not isinstance(bindlist, list):
        bindlist = bindlist.split(" ")

    for bind in bindlist:

        # Still cannot be None
        if bind:
            bot.debug("Adding bind %s" % bind)
            binds += ["--bind", bind]

            # Check that exists on host
            host = bind.split(":")[0]
            if not os.path.exists(host):
                bot.error("%s does not exist on host." % bind)
                sys.exit(1)

    return binds


def send_command(self, cmd, sudo=False, stderr=None, stdout=None):
    """send command is a non interactive version of run_command, meaning
    that we execute the command and return the return value, but don't
    attempt to stream any content (text from the screen) back to the
    user. This is useful for commands interacting with OCI bundles.

    Parameters
    ==========
    cmd: the list of commands to send to the terminal
    sudo: use sudo (or not)
    """

    if sudo:
        cmd = ["sudo"] + cmd

    process = subprocess.Popen(cmd, stderr=stderr, stdout=stdout)
    result = process.communicate()
    return result


def run_command(
    self,
    cmd,
    sudo=False,
    capture=True,
    quiet=None,
    return_result=False,
    sudo_options=None,
    environ=None,
):

    """run_command is a wrapper for the global run_command, checking first
    for sudo and exiting on error if needed. The message is returned as
    a list of lines for the calling function to parse, and stdout uses
    the parent process so it appears for the user.

    Parameters
    ==========
    cmd: the command to run
    sudo: does the command require sudo?
    quiet: if quiet set by function, overrides client setting.
    return_result: return the result, if not successful (default False).
    sudo_options: string or list of strings that will be passed as options to sudo
    On success, returns result.

    """
    # First preference to function, then to client setting
    if quiet is None:
        quiet = self.quiet

    result = run_cmd(
        cmd,
        sudo=sudo,
        capture=capture,
        quiet=quiet,
        sudo_options=sudo_options,
        environ=environ,
    )

    # If one line is returned, squash dimension
    if len(result["message"]) == 1:
        result["message"] = result["message"][0]

    # If the user wants to return the result, just return it
    if return_result:
        return result

    # On success, return result
    if result["return_code"] == 0:
        return result["message"]

    return result
