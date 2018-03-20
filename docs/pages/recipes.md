---
layout: default
title: Recipes
pdf: true
permalink: /recipes
toc: false
---

# Singularity Python Converters

We will here discuss the Singularity Python converters that will help you
to convert between recipe files. What kind of things might you want to do?

 - convert a Dockerfile to a Singularity Recipe
 - convert a Singularity Recipe to a Dockerfile (TBA)
 - read in a recipe of either type, and modify it before doing the above


# Command Line Client
You don't need to interact with Python to use the converter! It's sometimes 
much easier to use the command line and spit something out into the terminal,
for quick visual inspection or piping into an output file. If you use the 
`spython` utility, you can see your options available:


```
spython --help

Singularity Python [v0.0.21]

usage: spython [--debug] [--quiet] [--version] general usage ...

Singularity Client

optional arguments:
  --debug, -d    use verbose logging to debug.
  --quiet, -q    suppress all normal output
  --version      show singularity and spython version

actions:
  actions for Singularity

  general usage  description
    recipe       Recipe conversion and parsing
    shell        Interact with singularity python
    test         Container testing (TBD)
```

We can generate a *Singularity recipe* printed to the console by just providing 
the input Dockerfile

```
$ spython recipe Dockerfile
Bootstrap: docker
From: python:3.5.1
...
```

We could pipe that somewhere...

```
$ spython recipe Dockerfile >> Singularity.snowflake
```

Or give the filename to the function:

```
$ spython recipe Dockerfile Singularity.snowflake
WARNING /tmp/requirements.txt doesn't exist, ensure exists for build
WARNING requirements.txt doesn't exist, ensure exists for build
WARNING /code/ doesn't exist, ensure exists for build
Saving to Singularity.snowflake
```

The same can be done for converting a Dockerfile to Singularity

```
$ spython recipe Singularity >> Dockerfile
```

And don't forget you can interact with Docker images natively with Singularity!

```
$ singularity pull docker://ubuntu:latest
```


## Custom Generation
What else can we do, other than giving an input file and optional output file?
Let's ask for help for the "recipe" command:

```
$ spython recipe --help
usage: spython recipe [-h] [--entrypoint ENTRYPOINT] [files [files ...]]

positional arguments:
  files                 the recipe input file and [optional] output file

optional arguments:
  -h, --help            show this help message and exit
  --entrypoint ENTRYPOINT
                        define custom entry point and prevent discovery
```

See the `--entrypoint` argument? If you **don't** specify it, the recipe will be
written and use the Dockerfile `ENTRYPOINT` and then `CMD`, in that order. If 
neither of these exist, it defaults to `/bin/bash`. If you **do** specify it,
then your custom entrypoint will be used instead. For example, if I instead 
want to change the shell:

```
$ spython recipe --entrypoint /bin/sh Dockerfile
...
%runscript
exec /bin/sh "$@"
```

Notice that the last line (which usually defaults to `/bin/bash`) is what I 
specified. Finally, you can ask for help and print with more verbosity! Just ask for `--debug`

```
$ spython --debug recipe Dockerfile 
DEBUG Logging level DEBUG
DEBUG Singularity Python Version: 0.0.21
DEBUG [in]  FROM python:3.5.1
DEBUG FROM ['python:3.5.1']
DEBUG [in]  ENV PYTHONUNBUFFERED 1
DEBUG [in]  RUN apt-get update && apt-get install -y \
DEBUG [in]  RUN apt-get update && apt-get install -y \
DEBUG [in]  RUN git clone https://www.github.com/singularityware/singularity.git
DEBUG [in]  WORKDIR singularity
DEBUG [in]  RUN ./autogen.sh && ./configure --prefix=/usr/local && make && make install
DEBUG [in]  ADD requirements.txt /tmp/requirements.txt
WARNING requirements.txt doesn't exist, ensure exists for build
...
```
or less, ask for `--quiet`

```
$ spython --quiet recipe Dockerfile
```


# Python API

## Dockerfile Conversion
We will first review conversion of a Dockerfile, from within Python. 

### Load the Dockerfile
Let's say we are running Python interactively from our present working directory,
in which we have a Dockerfile. 

```
from spython.main.parse import DockerRecipe
recipe = DockerRecipe('Dockerfile')
```

If you don't have the paths locally that are specified in `ADD`, or `COPY` (this
might be the case if you are building on a different host) you will get a
warning.

```
WARNING /tmp/requirements.txt doesn't exist, ensure exists for build
WARNING requirements.txt doesn't exist, ensure exists for build
WARNING /code/ doesn't exist, ensure exists for build
```

That's all you need to do to load! The loading occurs when you create the object.
The finished object is a spython recipe

```
recipe
Out[2]: [spython-recipe][/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/Dockerfile]
```

and we can remember it's from a docker base

```
$ recipe.name
'docker'
```

It has all of the parsed sections from the Dockerfile,
named as you would expect them! These are generally lists and dictionary 
data structure that can be easily parsed into another recipe type. At this point 
you could inspect them, and modify as needed before doing the conversion.


```
$ recipe.environ
['PYTHONUNBUFFERED=1']

$ recipe.files
[['requirements.txt', '/tmp/requirements.txt'],
 ['/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli', '/code/']]

$ recipe.cmd
['/code/run_uwsgi.sh']

$ recipe.install
['PYTHONUNBUFFERED=1',
 '\n',
 '################################################################################\n',
 '# CORE\n',
 '# Do not modify this section\n']
...
```

Since Dockerfiles handle defining environment variables at build time and setting
them for the container at runtime, when we encounter an `ENV` section we add
the variable both to the `environ` list *and* as a command for the install 
section.

### Convert to Singularity Recipe
To do the conversion from the Dockerfile to a Singularity recipe, simply call 
"convert." This function estimates your desired output based on the input (i.e.,
a Dockerfile base is expected to be desired to convert to Singularity Recipe,
and vice versa). This will return a string to the console of your recipe.

```
result = recipe.convert()
print(result)

Bootstrap: docker
From: python:3.5.1
%files
requirements.txt /tmp/requirements.txt
/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli /code/
%labels
%post
PYTHONUNBUFFERED=1

################################################################################
# CORE
# Do not modify this section

apt-get update && apt-get install -y \
    pkg-config \
    cmake \
    openssl \
    wget \
    git \
    vim

apt-get update && apt-get install -y \
    anacron \
    autoconf \
    automake \
    libtool \
    libopenblas-dev \
    libglib2.0-dev \
    gfortran \
    libxml2-dev \
    libxmlsec1-dev \
    libhdf5-dev \
    libgeos-dev \
    libsasl2-dev \
    libldap2-dev \
    build-essential

# Install Singularity
git clone https://www.github.com/singularityware/singularity.git
cd singularity
./autogen.sh && ./configure --prefix=/usr/local && make && make install

# Install Python requirements out of /tmp so not triggered if other contents of /code change
pip install -r /tmp/requirements.txt


################################################################################
# PLUGINS
# You are free to comment out those plugins that you don't want to use

# Install LDAP (uncomment if wanted)
# RUN pip install python3-ldap
# RUN pip install django-auth-ldap


mkdir /code
mkdir -p /var/www/images

cd /code
apt-get remove -y gfortran

apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install crontab to setup job
echo "0 0 * * * /usr/bin/python /code/manage.py generate_tree" >> /code/cronjob
crontab /code/cronjob
rm /code/cronjob


# EXPOSE 3031
%environment
export PYTHONUNBUFFERED=1
%runscript
exec /code/run_uwsgi.sh "$@"
```

Note in the above because Singularity recipes do not understand labels like
`EXPOSE` and `VOLUME` they are commented out. 
You can also ask for a specific type, either of these would work.

```
recipe.convert(convert_to='docker')         # convert to Docker
recipe.convert(convert_to='singularity')    # convert to Singularity
```


### Save to Singularity Recipe
if you want to save to file, the same logic applies as above, except you can
use the "save" function. If you don't specify an output file, one will
be generated for you in the present working directory, a Singularity or 
Dockerfile with a randomly generated extension.

```
$ recipe.save()
Saving to Singularity.8q5lkg1n
```

And you can also name it whatever you like :)

```
$ recipe.save('Singularity.special-snowflake')
Saving to Singularity.special-snowflake
```

<hr>


## Singularity Conversion
We will do the same action, but in the opposite direction, convering a Singularity recipe
to a Dockerfile! This is a harder direction because we have to convert each line
from `%post` into a Dockerfile, and we are going from a "chunk" representation to
a "lines" one that warrants more detail. We do our best estimate of ordering by
doing the following:

 - files and labels come first, assuming that content should be added to the container at the beginning.
 - any change of directory (cd) at the beginning of a line is replaced with `WORKDIR`


### Load the Singularity Recipe


```
from spython.main.parse import SingularityRecipe
recipe = SingularityRecipe('Singularity')

FROM willmclaren/ensembl-vep
```

We know we have read in a Singularity file!

```
$ recipe.name
'singularity'
```

If you peek at the loaded configuration, you will see that it gets parsed into
the Singularity sections.

```
$ recipe.config 
{'comments': ['# sudo singularity build ensembl-vep Singularity'],
 'environment': ['LANGUAGE=en_US',
  'LANG="en_US.UTF-8"',
  'LC_ALL=C',
  'export LANGUAGE LANG LC_ALL',
  ''],
 'from': 'willmclaren/ensembl-vep',
 'help': ['This is a singularity file for VEP docker (v1)', ''],
 'labels': ['DARTH VADER', 'QUASI MODO', 'LizardLips NoThankYou', ''],
 'post': ['mkdir /.vep;',
  'mkdir /vep_genomes;',
  'git clone https://github.com/Ensembl/VEP_plugins.git;',
  'git clone https://github.com/griffithlab/pVAC-Seq.git;',
  'cp /pVAC-Seq/pvacseq/VEP_plugins/Wildtype.pm /VEP_plugins;',
  'rm -r /pVAC-Seq;',
  ''],
 'runscript': ['exec /home/vep/src/ensembl-vep/vep "$@"']}
```

### Convert to Dockerfile
You can then use the same convert function to generate your Dockerfile.

```
$ dockerfile = recipe.convert()
$ print(dockerfile)
print(recipe.convert())
FROM: willmclaren/ensembl-vep
# This is a singularity file for VEP docker (v1)
#  sudo singularity build ensembl-vep Singularity
LABEL DARTH VADER
LABEL QUASI MODO
LABEL LizardLips NoThankYou
ENV LANGUAGE=en_US
ENV LANG="en_US.UTF-8"
ENV LC_ALL=C
RUN mkdir /.vep;
RUN mkdir /vep_genomes;
RUN git clone https://github.com/Ensembl/VEP_plugins.git;
RUN git clone https://github.com/griffithlab/pVAC-Seq.git;
RUN cp /pVAC-Seq/pvacseq/VEP_plugins/Wildtype.pm /VEP_plugins;
RUN rm -r /pVAC-Seq;
CMD exec /home/vep/src/ensembl-vep/vep "$@"
```

or instead save it to file:

```
$ recipe.save('Dockerfile')
```

## Python Shell
You can also interact with the above functions most quickly via `spython shell`.

```
$ spython shell
Python 3.5.2 |Anaconda 4.2.0 (64-bit)| (default, Jul  2 2016, 17:53:06) 
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

```

The parser is added to the client, and you can use it just like before!

```
In [1]: parser = client.DockerRecipe('Dockerfile')
WARNING /tmp/requirements.txt doesn't exist, ensure exists for build
WARNING requirements.txt doesn't exist, ensure exists for build
WARNING /code/ doesn't exist, ensure exists for build
```
```
recipe = parser.convert()
print(recipe)
```

or do the same for Singularity:

```
$ parser = client.SingularityRecipe('Singularity')
$ recipe.convert()         # convert to Docker
```

<div>
    <a href="/singularity-cli/client"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/singularity-cli/contribute"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
