#!/usr/bin/python

# Copyright (C) 2017-2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from spython.main.parse.parsers import DockerParser, SingularityParser


def test_get_parser():
    from spython.main.parse.parsers import get_parser

    parser = get_parser('docker')
    assert parser == DockerParser

    parser = get_parser('Dockerfile')
    assert parser == DockerParser

    parser = get_parser('Singularity')
    assert parser == SingularityParser


def test_docker_parser(test_data):
    dockerfile = os.path.join(test_data['root'], 'Dockerfile')        
    parser = DockerParser(dockerfile)

    assert str(parser) == '[spython-parser][docker]'

    # Test all fields from recipe
    assert parser.recipe.fromHeader == 'python:3.5.1'
    assert parser.recipe.cmd == '/code/run_uwsgi.sh'
    assert parser.recipe.entrypoint is None
    assert parser.recipe.workdir == '/code'
    assert parser.recipe.volumes == []
    assert parser.recipe.ports == ['3031']
    assert parser.recipe.files[0] == ['requirements.txt', '/tmp/requirements.txt']
    assert parser.recipe.environ == ['PYTHONUNBUFFERED=1']
    assert parser.recipe.source == dockerfile

def test_singularity_parser(test_data):
    recipe = os.path.join(test_data['root'], 'Singularity')  
    parser = SingularityParser(recipe)

    assert str(parser) == '[spython-parser][singularity]'

    # Test all fields from recipe
    assert parser.recipe.fromHeader == 'continuumio/miniconda3'
    assert parser.recipe.cmd == 'exec /opt/conda/bin/spython "$@"'
    assert parser.recipe.entrypoint is None
    assert parser.recipe.workdir is None
    assert parser.recipe.volumes == []
    assert parser.recipe.files == []
    assert parser.recipe.environ == []
    assert parser.recipe.source == recipe
