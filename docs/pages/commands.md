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
<div>
    <a href="/singularity-cli/d"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/sregistry-cli/client"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
