#!/usr/bin/python

# Copyright (C) 2017-2021 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.main import Client
from spython.utils import write_file
import shutil
import os
import pytest
from subprocess import CalledProcessError


def test_build_from_docker(tmp_path):
    container = str(tmp_path / "container.sif")

    created_container = Client.build(
        "docker://busybox:1.30.1", image=container, sudo=False
    )
    assert created_container == container
    assert os.path.exists(created_container)


def test_export():
    sandbox = "busybox:1.30.sandbox"
    created_sandbox = Client.export("docker://busybox:1.30.1")
    assert created_sandbox == sandbox
    assert os.path.exists(created_sandbox)
    shutil.rmtree(created_sandbox)


def test_docker_pull(docker_container):
    tmp_path, container = docker_container
    print(container)
    ext = "sif" if Client.version_info().major >= 3 else "simg"
    assert container == str(tmp_path / ("busybox:1.30.1." + ext))
    assert os.path.exists(container)


def test_execute(docker_container):
    result = Client.execute(docker_container[1], "ls /")
    print(result)
    assert "tmp\nusr\nvar" in result


def test_execute_with_return_code(docker_container):
    result = Client.execute(docker_container[1], "ls /", return_result=True)
    print(result)
    assert "tmp\nusr\nvar" in result["message"]
    assert result["return_code"] == 0


@pytest.mark.parametrize("return_code", [True, False])
def test_execute_with_called_process_error(
    capsys, docker_container, return_code, tmp_path
):
    tmp_file = os.path.join(tmp_path, "CalledProcessError.sh")
    # "This is stdout" to stdout, "This is stderr" to stderr
    script = f"""#!/bin/bash
echo "This is stdout"
>&2 echo "This is stderr"
{"exit 1" if return_code else ""}
"""
    write_file(tmp_file, script)
    if return_code:
        with pytest.raises(CalledProcessError):
            for line in Client.execute(
                docker_container[1], f"/bin/sh {tmp_file}", stream=True
            ):
                print(line, "")
    else:
        for line in Client.execute(
            docker_container[1], f"/bin/sh {tmp_file}", stream=True
        ):
            print(line, "")
    captured = capsys.readouterr()
    assert "stdout" in captured.out
    if return_code:
        assert "stderr" in captured.err
    else:
        assert "stderr" not in captured.err


def test_inspect(docker_container):
    result = Client.inspect(docker_container[1])
    assert "attributes" in result or "data" in result
