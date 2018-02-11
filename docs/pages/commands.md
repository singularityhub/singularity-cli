---
layout: default
title: Getting Started
pdf: true
permalink: /commands
toc: false
---

# Python API
We will first discuss the Python API, meaning functions that you can use in python to work with 
Singularity images. Python is strong in the world of scientific programming, and so if you 
are reading these notes it's likely that you want to integrate Singularity containers into
your Python applications. We wrote you a client to do that!

**under development** 

 - [Scripts](#scripts) how to load the client from scratch in your Python script
 - [Pyshell](#pyshell) gives you an interactive python shell with a client 
 - [Pull](#pull) an image using Singularity
 - [Apps](#apps) list the [Scientific Filesystem](https://sci-f.github.io) apps in your image
 - [Inspect](#inspect) metadata about your image.
 - [Run](#run) execute the runscript for your image.


## Scripts
In most scripts, you can just import the client and go from there:

```
from spython.main import Client
```

You will find the actions that you are familiar with, along with a few extra:

```
$ Client. [TAB}                         
                Client.apps          Client.execute       Client.load          Client.run           
                Client.build         Client.help          Client.println       Client.version       
                Client.check_install Client.image         Client.pull                               
                Client.debug         Client.inspect       Client.quiet    
```

To get going with a Singularity image, just load it. It can be a file, or a uri to
reference a file.

```
$ Client.load('docker://vsoch/hello-world')
docker://vsoch/hello-world
```

But who wants to do this every time? I certainly don't. If you want an easier way to
interact with the client, just use the python shell, discussed next. 

## Pyshell
If you want to jump right in you can start a python shell (`pyshell`) to have a client ready to go!

```
$ spython pyshell
Python 3.5.2 |Anaconda 4.2.0 (64-bit)| (default, Jul  2 2016, 17:53:06) 
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.
```

The client is imported as client

```
$client
 [Singularity-Python]
```

At this point, you might want to load an image. An image can be a file, or a unique 
resource identifier (uri).

```
$ client.load('docker://vsoch/hello-world')
docker://vsoch/hello-world

$ client
$ [Singularity-Python][docker://vsoch/hello-world]
```

Notice about how the client shows the image is present. 
You can also shell in with an image "preloaded" and ready to interact with.

```
spython pyshell docker://ubuntu
Python 3.5.2 |Anaconda 4.2.0 (64-bit)| (default, Jul  2 2016, 17:53:06) 
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

$ client
 [Singularity-Python][docker://ubuntu]
```

And this is most logically the easiest entrypoint!


### Pull
If you are using Singularity to pull (and not the Singularity Global Client) the Singularity Python
provides a wrapper around that. We start with a shell with a client that has the `docker://ubuntu` image loaded and ready to go! 
[Here is a video](https://asciinema.org/a/162164?speed=2) of the example below if you want to watch instead of read.

```
spython shell docker://ubuntu
```
```
$ client.pull()
2.4.2-development.g706e90e
singularity pull --name vsoch-hello-world.simg shub://vsoch/hello-world
Progress |===================================| 100.0% 
Done. Container is at: /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/vsoch-hello-world.simg
vsoch-hello-world.simg
$ 'vsoch-hello-world.simg'
```

You can ask for a custom name:

```
client.pull(name='meatballs.simg')
```

and/or a custom pull folder to dump it:

```
client.pull(pull_folder='/tmp')
2.4.2-development.g706e90e
singularity pull --name vsoch-hello-world.simg shub://vsoch/hello-world
Progress |===================================| 100.0% 
Done. Container is at: /tmp/vsoch-hello-world.simg
/tmp/vsoch-hello-world.simg
$ '/tmp/vsoch-hello-world.simg'
```

For Singularity Hub images, you can also name by hash or commit.

```
client.pull(name_by_commit=True)
client.pull(name_by_hash=True)
```

Finally, you can ask to pull a different image.

```
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

Cool!

## Apps
We can inspect an image for a list of [SCIF](https://sci-f.github.io) apps that are installed within.
First, let's open a python shell with the client pre-loaded:

```
spython pyshell
```

and ask to see applications in an image:
```

In [1]: apps=client.apps('/home/vanessa/Desktop/image.simg')
2.4.2-development.g706e90e
bar
cat
dog
foo

$ apps
$ ['bar', 'cat', 'dog', 'foo']
```

We get a flat list of the application names. We can also get the full path to
their bases:

```
$ apps=client.apps('/home/vanessa/Desktop/image.simg', full_path=True)
2.4.2-development.g706e90e
bar
cat
dog
foo

$ ['/scif/apps/bar', '/scif/apps/cat', '/scif/apps/dog', '/scif/apps/foo']
```

## Inspect
Inspect will give us a json output of an image metadata. Let's load the pyshell with a client,
and also give it an image.

```
spython pyshell GodloveD-lolcow-master-latest.simg 
GodloveD-lolcow-master-latest.simg
```

Now inspect!

```
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

```
$ output = client.inspect('/home/vanessa/Desktop/image.simg', app='foo')
```

We could also ask for non-json "human friendly" output:

```
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

```
client.inspect('/home/vanessa/Desktop/image.simg')
```

## Run
Running is pretty intuitive. Just load an image into the client:

```
spython pyshell GodloveD-lolcow-master-latest.simg 
```
and then run it!

```
$ output = client.run()
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

You can also specify to run an app in an image:

```
$ client.load('/home/vanessa/Desktop/image.simg')
/home/vanessa/Desktop/image.simg

$ output = client.run(app='foo')

2.4.2-development.g706e90e
RUNNING FOO
```


<div>
    <a href="/singularity-cli/d"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/sregistry-cli/client"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
