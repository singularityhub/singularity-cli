# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.instance import Instance
from spython.logger import bot


def parse_table(table_string, header, remove_rows=1):
    """parse a table to json from a string, where a header is expected by default.
       Return a jsonified table.

       Parameters
       ==========
       table_string: the string table, ideally with a header
       header: header of expected table, must match dimension (number columns)
       remove_rows: an integer to indicate a number of rows to remove from top
                    the default is 1 assuming we don't want the header
    """
    rows = [x for x in table_string.split("\n") if x]
    rows = rows[0 + remove_rows :]

    # Parse into json dictionary
    parsed = []

    for row in rows:
        item = {}
        # This assumes no white spaces in each entry, which should be the case
        row = [x for x in row.split(" ") if x]
        for i, r in enumerate(row):
            item[header[i]] = r
        parsed.append(item)
    return parsed


def get(self, name, return_json=False, quiet=False, singularity_options=None):
    """get is a list for a single instance. It is assumed to be running,
       and we need to look up the PID, etc.
    """
    from spython.utils import check_install

    check_install()

    # Ensure compatible for singularity prior to 3.0, and after 3.0
    subgroup = "instance.list"

    if "version 3" in self.version():
        subgroup = ["instance", "list"]

    cmd = self._init_command(subgroup, singularity_options)

    cmd.append(name)
    output = self.run_command(cmd, quiet=True)

    # Success, we have instances

    if output["return_code"] == 0:

        # Only print the table if we are returning json
        if not quiet:
            print("".join(output["message"]))

        # Prepare json result from table

        header = ["daemon_name", "pid", "container_image"]
        instances = parse_table(output["message"][0], header)

        # Does the user want instance objects instead?
        listing = []
        if not return_json:
            for i in instances:
                new_instance = Instance(
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
    if name is not None and len(instances) == 1:
        instances = instances[0]

    return instances
