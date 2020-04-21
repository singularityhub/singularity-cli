# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


from spython.logger import bot
from spython.utils import run_command


def list_instances(
    self,
    name=None,
    return_json=False,
    quiet=False,
    sudo=False,
    singularity_options=None,
):
    """list instances. For Singularity, this is provided as a command sub
       group.

       singularity instance.list

       Return codes provided are different from standard linux:
       see https://github.com/singularityware/singularity/issues/1706

       Parameters
       ==========
       return_json: return a json list of instances instead of objects (False)
       name: if defined, return the list for just one instance (used to ged pid)
       singularity_options: a list of options to provide to the singularity client

       Return Code  --   Reason
       0 -- Instances Found
       1 -- No Instances, libexecdir value not found, functions file not found
       255 -- Couldn't get UID

    """
    from spython.instance.cmd.iutils import parse_table
    from spython.utils import check_install

    check_install()

    subgroup = "instance.list"

    if "version 3" in self.version():
        subgroup = ["instance", "list"]

    cmd = self._init_command(subgroup, singularity_options)

    # If the user has provided a name, we want to see a particular instance
    if name is not None:
        cmd.append(name)

    output = run_command(cmd, quiet=True, sudo=sudo)
    instances = []

    # Success, we have instances

    if output["return_code"] == 0:

        # Only print the table if we are returning json
        if not quiet:
            print("".join(output["message"]))

        # Prepare json result from table
        # Singularity after 3.5.2 has an added ipaddress
        try:
            header = ["daemon_name", "pid", "container_image"]
            instances = parse_table(output["message"][0], header)
        except:
            header = ["daemon_name", "pid", "ip", "container_image"]
            instances = parse_table(output["message"][0], header)

        # Does the user want instance objects instead?
        listing = []
        if not return_json:
            for i in instances:

                # If the user has provided a name, only add instance matches
                if name is not None:
                    if name != i["daemon_name"]:
                        continue

                # Otherwise, add instances to the listing
                new_instance = self.instance(
                    pid=i["pid"],
                    name=i["daemon_name"],
                    image=i["container_image"],
                    start=False,
                )

                listing.append(new_instance)
            instances = listing

    # Couldn't get UID

    elif output["return_code"] == 255:
        bot.error("Couldn't get UID")

    # Return code of 0
    else:
        bot.info("No instances found.")

    # If we are given a name, return just one
    if name is not None and instances not in [None, []]:
        if len(instances) == 1:
            instances = instances[0]

    return instances


def stopall(self, sudo=False, quiet=True, singularity_options=None):
    """stop ALL instances. This command is only added to the command group
       as it doesn't make sense to call from a single instance

       Parameters
       ==========
       sudo: if the command should be done with sudo (exposes different set of
             instances)

    """
    from spython.utils import check_install

    check_install()

    subgroup = "instance.stop"

    if "version 3" in self.version():
        subgroup = ["instance", "stop"]

    cmd = self._init_command(subgroup, singularity_options)
    cmd = cmd + ["--all"]
    output = run_command(cmd, sudo=sudo, quiet=quiet)

    if output["return_code"] != 0:
        message = "%s : return code %s" % (output["message"], output["return_code"])
        bot.error(message)
        return output["return_code"]

    return output["return_code"]
