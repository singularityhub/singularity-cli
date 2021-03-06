#!/usr/bin/python

# Copyright (C) 2017-2021 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from spython.main import Client


def test_instance_class():
    instance = Client.instance("docker://ubuntu", start=False)
    assert instance.get_uri() == "instance://" + instance.name
    assert instance.name != ""

    name = "coolName"
    instance = Client.instance("docker://busybox:1.30.1", start=False, name=name)
    assert instance.get_uri() == "instance://" + instance.name
    assert instance.name == name


def test_has_no_instances():
    instances = Client.instances()
    assert instances == []


class TestInstanceFuncs(object):
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        Client.instance_stopall()

    def test_instance_cmds(self, docker_container):
        image = docker_container[1]
        myinstance = Client.instance(image)
        assert myinstance.get_uri().startswith("instance://")

        print("...Case 2: List instances")
        instances = Client.instances()
        assert len(instances) == 1
        instances = Client.instances(return_json=True)
        assert len(instances) == 1
        assert isinstance(instances[0], dict)

        print("...Case 3: Commands to instances")
        result = Client.execute(myinstance, ["echo", "hello"])
        assert result == "hello\n"

        print("...Case 4: Return value from instance")
        result = Client.execute(myinstance, "ls /", return_result=True)
        print(result)
        assert "tmp\nusr\nvar" in result["message"]
        assert result["return_code"] == 0

        print("...Case 5: Stop instances")
        myinstance.stop()
        instances = Client.instances()
        assert instances == []
        myinstance1 = Client.instance(image)
        myinstance2 = Client.instance(image)
        assert myinstance1 is not None
        assert myinstance2 is not None
        instances = Client.instances()
        assert len(instances) == 2
        Client.instance_stopall()
        instances = Client.instances()
        assert instances == []
