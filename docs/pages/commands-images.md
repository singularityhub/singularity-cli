---
layout: default
title: Image Commands
pdf: true
permalink: /commands-images
toc: false
---

This section focuses on commands to interact with containers, the base and core of
using Singularity. The client and examples below will show you how to
integrate Singularity into your scientific Python applications.


 - [Scripts](#scripts) how to load the client from scratch in your Python script
 - [Shell](#shell) gives you an interactive python shell with a client

From within python, you can then use the following functions to control Singularity:

 - [Build](#build) an image from a recipe.
 - [Pull](#pull) an image using Singularity
 - [Apps](#apps) list the [Scientific Filesystem](https://sci-f.github.io) apps in your image
 - [Inspect](#inspect) metadata about your image.
 - [Run](#run) execute the runscript for your image.
 - [Execute](#execute) execute a command to the container
 - [Help](#help) easily show help documentation for commands
 - [Fun](#fun) Want to have a little fun? The robots got your back :)


Importantly, `run`, `exec`, `pull` and `build` supporting [streaming](#streaming)
responses, meaning that they return generators that you can use in your applications.

<hr>

## Scripts
In most scripts, you can just import the client and go from there:

```python
from spython.main import Client
```

You will find the actions that you are familiar with, along with a few extra:

```python
> Client. [TAB}
                Client.apps          Client.execute       Client.load          Client.run
                Client.build         Client.help          Client.println       Client.version
                Client.check_install Client.image         Client.pull
                Client.debug         Client.inspect       Client.quiet
```

To get going with a Singularity image, just load it. It can be a file, or a uri to
reference a file.

```python
> Client.load('docker://vsoch/hello-world')
docker://vsoch/hello-world
```

But who wants to do this every time? I certainly don't. If you want an easier way to
interact with the client, just use the python shell, discussed next.

<hr>

## Shell
If you want to jump right in you can start a python shell (`shell`) to have a client ready to go!

```python
> spython shell
Python 3.5.2 |Anaconda 4.2.0 (64-bit)| (default, Jul  2 2016, 17:53:06)
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.
```

The client is imported as client

```python
> client
 [Singularity-Python]
```

At this point, you might want to load an image. An image can be a file, or a unique
resource identifier (uri).

```python
> client.load('docker://vsoch/hello-world')
docker://vsoch/hello-world

> client
> [Singularity-Python][docker://vsoch/hello-world]
```

Notice about how the client shows the image is present.
You can also shell in with an image "preloaded" and ready to interact with.

```python
spython shell docker://ubuntu
Python 3.5.2 |Anaconda 4.2.0 (64-bit)| (default, Jul  2 2016, 17:53:06)
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

> client
 [Singularity-Python][docker://ubuntu]
```

And this is most logically the easiest entrypoint!  Note that this is **not**
 the Singularity shell, so it doesn't have custom binds, etc. You would
specify them from the shell using the client.


<hr>

## Build
You likely want to build images, but from within Python. The Singularity Python API allows
you to do this. You can customize the recipe, container name, and location.


| variable     |  example                                 |  default |               description  |
|--------------|------------------------------------------|----------|----------------------------|
| recipe       | `docker://ubuntu:latest`, `Singularity`  | None     | the base for the build. If not defined, we look for a Singularity recipe in the `$PWD` |
| image        | /opt/dinosaur.simg                       | None     | the image to build. If None, derive from recipe, or robot name  |
| isolated     |  singularity build --isolated ...        | False    | create an isolated build environment |
| sandbox      |  singularity build --sandbox ...         | False    | build a sandbox image |
| writable     |  singularity build --writable ...        | False    | build a writable image  |
| build_folder | /tmp                                     | None     | if set, build in folder instead of `$PWD` |
| ext          | `simg`                                   | `simg`   | The extension to use for the image, if name not provided |
| robot_name   | boolean                                  | False    | If True, generate a robot name for the image instead of default based on uri |
| sudo         |                                          | True     | use sudo to run the command |


First, let's open up an interactive shell with a client and docker uri already loaded.

```python
> spython shell docker://busybox:latest
docker://busybox:latest
```

Now let's build it. We are going to not provide any image name, or even input the
docker uri again.

```python
> client.build()
2.4.2-development.g706e90e
Building into existing container: busybox:latest.simg
Docker image path: index.docker.io/library/busybox:latest
Cache folder set to /root/.singularity/docker
Importing: base Singularity environment
Building Singularity FS image...
Building Singularity SIF container image...
Singularity container built: busybox:latest.simg
Cleaning up...
 'busybox:latest.simg'
```

Ask for a robot name.

```python
> client.build(robot_name=True)
2.4.2-development.g706e90e
Docker image path: index.docker.io/library/busybox:latest
Cache folder set to /root/.singularity/docker
Importing: base Singularity environment
Building Singularity FS image...
Building Singularity SIF container image...
Singularity container built: chunky-toaster-8054.simg
Cleaning up...
 'chunky-toaster-8054.simg'
```

Build with your own name:

```python
> client.build(image="meatballs.simg")
...
Singularity container built: meatballs.simg
Cleaning up...
 'meatballs.simg'
```

Ask for a custom build folder:

```python
client.build(build_folder='/tmp',robot_name=True)
...
Singularity container built: /tmp/crusty-peas-9436.simg
Cleaning up...
> '/tmp/crusty-peas-9436.simg'
```

If you didn't load the image, just specify it instead. here is an example of
building a sandbox (which requires sudo):

```python
> client.build('docker://debian:buster-slim', 'debian/', sandbox=True, sudo=True)
```

If you want to provide additional options, you can do so with `options`:

```python
> client.build('docker://debian:buster-slim', 'debian/', sandbox=True, options=["--fakeroot"])
```

<hr>

## Pull
If you are using Singularity to pull (and not the Singularity Global Client) the Singularity Python
provides a wrapper around that. We start with a shell with a client that has the `docker://ubuntu` image loaded and ready to go!
[Here is a video](https://asciinema.org/a/162164?speed=2) of the example below if you want to watch instead of read.

```python
spython shell docker://ubuntu
```
```python
> client.pull()
2.4.2-development.g706e90e
singularity pull --name vsoch-hello-world.simg shub://vsoch/hello-world
Progress |===================================| 100.0%
Done. Container is at: /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/vsoch-hello-world.simg
vsoch-hello-world.simg
> 'vsoch-hello-world.simg'
```

You can ask for a custom name:

```python
client.pull(name='meatballs.simg')
```

and/or a custom pull folder to dump it:

```python
client.pull(pull_folder='/tmp')
2.4.2-development.g706e90e
singularity pull --name vsoch-hello-world.simg shub://vsoch/hello-world
Progress |===================================| 100.0%
Done. Container is at: /tmp/vsoch-hello-world.simg
/tmp/vsoch-hello-world.simg
> '/tmp/vsoch-hello-world.simg'
```

You can add `force` to force an overwrite, if the file exists.

```python
> client.pull(pull_folder='/tmp', force=True)
```

For Singularity Hub images, you can also name by hash or commit.

``` python
client.pull(name_by_commit=True)
client.pull(name_by_hash=True)
```

You can ask to pull a different image.

```python
client.pull('docker://ubuntu')
 client.pull('docker://ubuntu')
2.4.2-development.g706e90e
singularity pull --name ubuntu.simg docker://ubuntu
Docker image path: index.docker.io/library/ubuntu:latest
Cache folder set to /home/vanessa/.singularity/docker
Importing: base Singularity environment
Building Singularity FS image...
...
```

Finally, the pull command supports generating an iterator! This means that you
can have a generator to return to some webby view to return the lines one by one to
the user.

```python

# Create the generator!
image, puller = client.pull('docker://ubuntu', stream=True, pull_folder='/tmp')
print(image)
# /tmp/ubuntu.simg
print(puller)
<generator object stream_command at 0x7f140c520eb8>

# Use it
for line in puller:
    print(line)

```
You could imagine streaming the above lines to a view, or appending to a list!
You can use this however is appropriate for your application. Cool!

<hr>


## Apps

We can inspect an image for a list of [SCIF](https://sci-f.github.io) apps that are installed within.
First, let's open a python shell with the client pre-loaded:

```python
spython shell
```

and ask to see applications in an image:
```

In [1]: apps=client.apps('/home/vanessa/Desktop/image.simg')
2.4.2-development.g706e90e
bar
cat
dog
foo

> apps
> ['bar', 'cat', 'dog', 'foo']
```

We get a flat list of the application names. We can also get the full path to
their bases:

```python
> apps=client.apps('/home/vanessa/Desktop/image.simg', full_path=True)
2.4.2-development.g706e90e
bar
cat
dog
foo

> ['/scif/apps/bar', '/scif/apps/cat', '/scif/apps/dog', '/scif/apps/foo']
```

<hr>


## Inspect
Inspect will give us a json output of an image metadata. Let's load the shell with a client,
and also give it an image.

```python
spython shell GodloveD-lolcow-master-latest.simg
GodloveD-lolcow-master-latest.simg
```

Now inspect!

```python
In [1]: result = client.inspect()
2.4.2-development.g706e90e
{
    "data": {
        "attributes": {
            "deffile": "BootStrap: docker\nFrom: ubuntu:16.04\n\n%post\n    apt-get -y update\n    apt-get -y install fortune cowsay lolcat\n\n%environment\n    export LC_ALL=C\n    export PATH=/usr/games:$PATH\n\n%runscript\n    fortune | cowsay | lolcat\n",
            "help": null,
            "labels": {
                "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
                "org.label-schema.usage.singularity.deffile": "Singularity",
                "org.label-schema.schema-version": "1.0",
                "org.label-schema.usage.singularity.deffile.from": "ubuntu:16.04",
                "org.label-schema.build-date": "2017-10-17T19:23:53+00:00",
                "org.label-schema.usage.singularity.version": "2.4-feature-squashbuild-secbuild.g217367c",
                "org.label-schema.build-size": "336MB"
            },
            "environment": "# Custom environment shell code should follow\n\n    export LC_ALL=C\n    export PATH=/usr/games:$PATH\n\n",
            "runscript": "#!/bin/sh \n\n    fortune | cowsay | lolcat\n",
            "test": null
        },
        "type": "container"
    }
}
```
You can inspect a single app:

```python
> output = client.inspect('/home/vanessa/Desktop/image.simg', app='foo')
```

We could also ask for non-json "human friendly" output:

```python
BootStrap: docker
From: ubuntu:16.04

%post
    apt-get -y update
    apt-get -y install fortune cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    fortune | cowsay | lolcat
{
    "status": 404,
    "detail": "This container does not have a helpfile",
    "title": "Help Undefined"
}
{
    "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
    "org.label-schema.usage.singularity.deffile": "Singularity",
    "org.label-schema.schema-version": "1.0",
    "org.label-schema.usage.singularity.deffile.from": "ubuntu:16.04",
    "org.label-schema.build-date": "2017-10-17T19:23:53+00:00",
    "org.label-schema.usage.singularity.version": "2.4-feature-squashbuild-secbuild.g217367c",
    "org.label-schema.build-size": "336MB"
}
# Custom environment shell code should follow

    export LC_ALL=C
    export PATH=/usr/games:$PATH

#!/bin/sh

    fortune | cowsay | lolcat
{
    "status": 404,
    "detail": "This container does not have any tests defined",
    "title": "Tests Undefined"
}
```

or a different image all together!

```python
client.inspect('/home/vanessa/Desktop/image.simg')
```

<hr>

## Run
Running is pretty intuitive. Just load an image into the client:

```bash
spython shell GodloveD-lolcow-master-latest.simg
```
and then run it!

```python
> output = client.run()
2.4.2-development.g706e90e
 _________________________________________
/ Behold, the fool saith, "Put not all    \
| thine eggs in the one basket"--which is |
| but a manner of saying, "Scatter your   |
| money and your attention;" but the wise |
| man saith, "Put all your eggs in the    |
| one basket and--WATCH THAT BASKET."     |
|                                         |
| -- Mark Twain, "Pudd'nhead Wilson's     |
\ Calendar"                               /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

### Run an App
You can also specify to run an app in an image:

```python
> client.load('/home/vanessa/Desktop/image.simg')
/home/vanessa/Desktop/image.simg

> output = client.run(app='foo')

2.4.2-development.g706e90e
RUNNING FOO
```

<hr>

## Execute
An `execute` maps to the Singularity `exec` and is like a run, but with a specific executable or entry point defined for the container.
Again, let's start with an image loaded in the client Python shell.

```python
spython shell /home/vanessa/Desktop/image.simg
/home/vanessa/Desktop/image.simg
```
Now let's try a basic `ls`. Note that the command is given as a list.

```python
> output = client.execute(['ls'])
2.4.2-development.g706e90e
CHANGELOG.md
CONTRIBUTING.md
...
vsoch-hello-world.simg
```
Now let's give more than one word in the command to demonstrate the list fully. Here we want
to echo "Hello!" to the console.

```python
> output = client.execute(['echo','"hello!"'])
2.4.2-development.g706e90e
"hello!"
```
and do the same, but with a different image specified.

```python
> client.execute('GodloveD-lolcow-master-latest.simg',['echo','"hello!"'])
2.4.2-development.g706e90e
"hello!"
```
Note that when you specify a new image, the old one isn't unloaded to replace it. If you
want this to happen, you would need to load it.

```python
> client.load('GodloveD-lolcow-master-latest.simg')
GodloveD-lolcow-master-latest.simg

> client
[Singularity-Python][GodloveD-lolcow-master-latest.simg]
```

<hr>

## Run and Exec Options
The commands that you can specify are as you would expect, coinciding with Singularity.

### Extra Options

You can add writable to a command or runscript execution. Here is touching a file in a sandbox.

```python
> client.execute('debian/', 'touch /file', writable=True, sudo=True)
[]
```
If you want to get the full result along with the return code, ask for it:

```python
> client.execute('debian/', 'touch /file', writable=True, sudo=True, return_result=True)
 {'message': [], 'return_code': 0}
```

or you can add a list of options. Here is adding `--writable-tmpfs` that is available
for Singularity 3.2.0 and later with run and exec:

```python
client.execute('debian', 'touch /tmp/file',  options=['--writable-tmpfs'])
```

Notice for the above we didn't need to use `--writable` because we have a writable
temporary filesystem.


### Bind Volumes
Here are many different ways you can specify binds:

```python
mkdir -p /tmp/avocado
touch /tmp/avocado/seed.txt

> client.load('/home/vanessa/Desktop/image.simg')
/home/vanessa/Desktop/image.simg

# Without the bind, opt is empty
> client.execute(['ls', '/opt'])
()

# Create the bind
> client.execute(['ls', '/opt'], bind='/tmp/avocado:/opt')
seed.txt
```
Note that the bind argument can take the form of any of the following, either
list or string:


```python
['/host:/container', '/both'] --> ["--bind", "/host:/container","--bind","/both" ]
['/both']                     --> ["--bind", "/both"]
'/host:container'             --> ["--bind", "/host:container"]
None                         --> []
```


| variable     | example                                    | default  |           description       |
|--------------|------------------------------------------  |----------|----------------------------|
| bind         |  add one or more --bind as a list or string| None     | one or more bind mounts |
| contain      |  add the --contain flag                    | False    | contain the environment and mounts |
| writable     |  singularity build --writable              | False    | build a writable image  |

Note that these are also provided for `exec` below.

### Run and Exec Streaming
If you want to run or execute a command, right now we've shown you how to do this:

```python
spython shell

# Pull a container to play with
> image = client.pull('docker://godlovedc/lolcow')
# 'godlovedc-lolcow.simg'

# Execute a command!
> client.execute(image, ['echo','hello','world'])
2.4.5-master.g0b17e18
hello world
Out[1]: 'hello world\n
```

Notice how it happens immediately, and you get the response back all at once? What
if you want to stream it? Add `stream=True`:

```python
executor = client.execute(image, ['echo','hello','world'], stream=True)
# <generator object stream_command at 0x7f3d384e6410>
for line in executor:
    print(line)

hello world
```

This might be useful if you want to return output line by line, or just append
each line of output to a list, or check it in some way.

## Help
If you are working in the console and desperate for some help, just ask for it:

```python
$ help = client.help()
2.4.2-development.g706e90e
USAGE: singularity [global options...] <command> [command options...] ...

GLOBAL OPTIONS:
    -d|--debug    Print debugging information
    -h|--help     Display usage summary
    -s|--silent   Only print errors
    -q|--quiet    Suppress all normal output
       --version  Show application version
    -v|--verbose  Increase verbosity +1
    -x|--sh-debug Print shell wrapper debugging information

GENERAL COMMANDS:
    help       Show additional help for a command or container
    selftest   Run some self tests for singularity install

CONTAINER USAGE COMMANDS:
    exec       Execute a command within container
    run        Launch a runscript within container
    shell      Run a Bourne shell within container
    test       Launch a testscript within container

CONTAINER MANAGEMENT COMMANDS:
    apps       List available apps within a container
    bootstrap  *Deprecated* use build instead
    build      Build a new Singularity container
    check      Perform container lint checks
    inspect    Display container's metadata
    mount      Mount a Singularity container image
    pull       Pull a Singularity/Docker container to $PWD
    siflist    list data object descriptors of a SIF container image
    sign       Sign a group of data objects in container
    verify     Verify the crypto signature of group of data objects in container

COMMAND GROUPS:
    capability User's capabilities management command group
    image      Container image command group
    instance   Persistent instance command group


CONTAINER USAGE OPTIONS:
    see singularity help <command>

For any additional help or support visit the Singularity
website: http://singularity.lbl.gov/

```

or ask for a specific command:

```python
> help = client.help('bootstrap')
2.4.2-development.g706e90e
USAGE: singularity [...] bootstrap <container path> <definition file>
******************************************************************************
NOTICE: The bootstrap command is deprecated and will be removed in a later
        release. bootstrap now uses the build command to create a writable
        container via the following syntax:

> singularity build -w container.img recipe.def

        You should update your usage accordingly.
******************************************************************************

```

Good to know!


<hr>

## Streaming
Streaming is available for `run`, `exec`, `build`, and `pull`. By adding `stream=True`
to the call you can return a generator to iterate over, and expose the result one line
at a time.

### Pull Stream
Here is the standard way of doing it. The output prints to the console, and the function
returns the image generated.

```python
spython shell

# Pull a container to play with
> image = client.pull('docker://godlovedc/lolcow')
# 'godlovedc-lolcow.simg'
```

What if you want to retrieve the output? Just make a generator! Note that when
you use the pull generator, you will get back the expected image name along with
the generator object.

```python
> image, puller = client.pull('docker://godlovedc/lolcow', stream=True, force=True)
# 'godlovedc-lolcow.simg'
# <generator object stream_command at 0x7f3d38f73fc0>
```
Let's say we want to get the lines of output in a list. You could do this.

```python
lines = []
for line in puller:
    lines.append(line)
```
```
lines
Out[22]:
[...
 'Singularity container built: ./godlovedc-lolcow.simg\n',
 'Cleaning up...\n',
 'Done. Container is at: ./godlovedc-lolcow.simg\n']
```

### Build Stream
The same case is true for build. We can stream the output and get it line by line.

```python
> image, builder = client.build(recipe='docker://godlovedc/lolcow',
                                stream=True,
                                robot_name=True)

# image (oh my)
# 'butterscotch-leg-4205.simg'

# builder
<generator object stream_command at 0x7f3d384e60a0>
```
```python
for line in builder:
    print(line, end='')
```

### Execute Stream
We can stream the output for execute and run just like pull.

```python
spython shell

# Pull a container to play with
> image = client.pull('docker://godlovedc/lolcow')
# 'godlovedc-lolcow.simg'

# Execute a command!
> client.execute(image, ['echo','hello','world'])
2.4.5-master.g0b17e18
hello world
Out[1]: 'hello world\n
```

Notice how it happens immediately, and you get the response back all at once? What
if you want to stream it? Add `stream=True`:

```python
executor = client.execute(image, ['echo','hello','world'], stream=True)
# <generator object stream_command at 0x7f3d384e6410>
for line in executor:
    print(line)

hello world
```

This might be useful if you want to return output line by line, or just append
each line of output to a list, or check it in some way.


### Run Stream
Finally, run is just executing the runscript, so it works the same.

```python
runner = client.run(image, stream=True)
# <generator object stream_command at 0x7f3d38f73728>
```
```
for line in runner:
    print(line, end='')

 ________________________________________
< Your supervisor is thinking about you. >
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
Uhoh.

# Pull a container to play with
> image = client.pull('docker://godlovedc/lolcow')
# 'godlovedc-lolcow.simg'

# Execute a command!
> client.execute(image, ['echo','hello','world'])
2.4.5-master.g0b17e18
hello world
Out[1]: 'hello world\n
```

Notice how it happens immediately, and you get the response back all at once? What
if you want to stream it? Add `stream=True`:

```python
executor = client.execute(image, ['echo','hello','world'], stream=True)
# <generator object stream_command at 0x7f3d384e6410>
for line in executor:
    print(line)

hello world
```


<hr>

## Fun
Want to have a little fun?

```bash
spython shell
```
```python
for i in range(10):
    print(client.RobotNamer.generate())

phat-truffle-5574
chunky-leg-2481
bricky-omelette-4994
frigid-cat-1600
boopy-gato-5761
rainbow-milkshake-7724
cowy-puppy-5847
chocolate-lamp-6383
quirky-leopard-1958
scruptious-egg-4612
```

Or <a href="https://asciinema.org/a/162228" target="_blank">view and use the Docker and Singularity images.</a>

<div>
    <a href="/singularity-cli/commands"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/singularity-cli/contribute"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
