#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from spython.main import Client
import shutil
import os


def test_build_from_docker(tmp_path):
    container = str(tmp_path / "container.sif")

    created_container = Client.build('docker://busybox:1.30.1', 
                                     image=container,
                                     sudo=False)
    assert created_container == container
    assert os.path.exists(created_container)

def test_export():
    sandbox = "busybox:1.30.sandbox"
    created_sandbox = Client.export('docker://busybox:1.30.1')
    assert created_sandbox == sandbox
    assert os.path.exists(created_sandbox)
    shutil.rmtree(created_sandbox)

def test_pull_and_run(tmp_path):
    image = Client.pull("shub://vsoch/singularity-images", 
                        pull_folder=str(tmp_path))
    print(image)
    assert os.path.exists(image)
    ext = 'sif' if Client.version_info().major >= 3 else 'simg'
    assert image == str(tmp_path / ('singularity-images.' + ext))

    result = Client.run(image)
    print(result)
    assert 'You say please, but all I see is pizza..' in result

def test_docker_pull(docker_container):
    tmp_path, container = docker_container
    print(container)
    ext = 'sif' if Client.version_info().major >= 3 else 'simg'
    assert container == str(tmp_path / ("busybox:1.30.1." + ext))
    assert os.path.exists(container)

def test_execute(docker_container):
    result = Client.execute(docker_container[1], 'ls /')
    print(result)
    assert 'tmp\nusr\nvar' in result

def test_execute_with_return_code(docker_container):
    result = Client.execute(docker_container[1], 'ls /', return_result=True)
    print(result)
    assert 'tmp\nusr\nvar' in result['message']
    assert result['return_code'] == 0

def test_inspect(docker_container):
    result = Client.inspect(docker_container[1])
    assert result['type'] == 'container'
    assert 'attributes' in result
