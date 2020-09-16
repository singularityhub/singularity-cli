# Copyright (C) 2017-2020 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


def generate_oci_commands():
    """The oci command group will allow interaction with an image using
    OCI commands.
    """
    from spython.oci import OciImage

    from spython.main.base.logger import println

    # run_command uses run_cmd, but wraps to catch error
    from spython.main.base.command import run_command, send_command
    from spython.main.base.generate import RobotNamer

    # Oci Command Groups
    from .mounts import mount, umount
    from .states import kill, state, start, pause, resume, _state_command
    from .actions import attach, create, delete, execute, run, _run, update

    # Oci Commands
    OciImage.start = start
    OciImage.mount = mount
    OciImage.umount = umount
    OciImage.state = state
    OciImage.resume = resume
    OciImage.pause = pause
    OciImage.attach = attach
    OciImage.create = create
    OciImage.delete = delete
    OciImage.execute = execute
    OciImage.update = update
    OciImage.kill = kill
    OciImage.run = run
    OciImage._run = _run
    OciImage._state_command = _state_command

    OciImage.RobotNamer = RobotNamer()
    OciImage._send_command = send_command  # send and disregard stderr, stdout
    OciImage._run_command = run_command
    OciImage._println = println
    OciImage.OciImage = OciImage

    return OciImage
