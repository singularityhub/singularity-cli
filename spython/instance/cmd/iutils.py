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


def parse_table(table_string, header, remove_rows=1):
    '''parse a table to json from a string, where a header is expected by default.
       Return a jsonified table.

       Parameters
       ==========
       table_string: the string table, ideally with a header
       header: header of expected table, must match dimension (number columns)
       remove_rows: an integer to indicate a number of rows to remove from top
                    the default is 1 assuming we don't want the header
    '''
    rows = [x for x in table_string.split('\n') if x]
    rows = rows[0+remove_rows:]

    # Parse into json dictionary
    parsed = []

    for row in rows:
        item = {}
        # This assumes no white spaces in each entry, which should be the case
        row = [x for x in row.split(' ') if x]
        for e in range(len(row)):
            item[header[e]] = row[e]
        parsed.append(item)
    return parsed


def get(self, name, return_json=False, quiet=False):
    '''get is a list for a single instance. It is assumed to be running,
       and we need to look up the PID, etc.
    '''
    from spython.utils import check_install
    check_install()

    cmd = self._init_command('instance.list')
    cmd.append(name)
    output = run_command(cmd, quiet=True)

    # Success, we have instances

    if output['return_code'] == 0:

        # Only print the table if we are returning json
        if quiet is False:
            print(''.join(output['message']))

        # Prepare json result from table

        header = ['daemon_name','pid','container_image']
        instances = parse_table(output['message'][0], header)

        # Does the user want instance objects instead?
        listing = []
        if return_json is False:
            for i in instances:
                new_instance = Instance(pid=i['pid'],
                                        name=i['daemon_name'],
                                        image=i['container_image'],
                                        start=False)

                listing.append(new_instance)
            instances = listing

    # Couldn't get UID

    elif output['return_code'] == 255:
        bot.error("Couldn't get UID")
        
    # Return code of 0
    else:
        bot.info('No instances found.')

    # If we are given a name, return just one
    if name is not None and len(instances) == 1:
        instances = instances[0]

    return instances

