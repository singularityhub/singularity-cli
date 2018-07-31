#
# This file is used to setup a build/devel environment for those using the Nix package manager
#

with import <nixpkgs> {};
with pkgs.python36Packages;
stdenv.mkDerivation {
  name = "impurePythonEnv";
  buildInputs = [
    libuuid
    singularity
    squashfsTools
    # these packages are required for virtualenv and pip to work:
    #
    python36Full
    python36Packages.virtualenv
    python36Packages.pip
    # pipenv
    # the following packages are related to the dependencies of your python
    # project.
    # In this particular example the python modules listed in the
    # requirements.tx require the following packages to be installed locally
    # in order to compile any binary extensions they may require.
    #
    # glibcLocales # for click+python3
    openssl
    # pyre # for typechecking
  ];
  src = null;
  shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
    export LANG=en_US.UTF-8
    virtualenv venv
    source venv/bin/activate
    export PYTHONPATH=$PWD
    echo "PYTHON VERSION"
    which python
    pip install -r requirements.txt
    pip install -r requirements-dev.txt    
    python setup.py sdist && python setup.py install
     
  '';
}

#    
#
# Now you can run the following command to start the server:
#
