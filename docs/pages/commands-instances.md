---
layout: default
title: Instance Commands
pdf: true
permalink: /commands-instances
toc: false
---

This section will discuss interaction with container instances, which generally
includes starting, stopping and running. From within python, you can instantiate
an sphython client, and then use the following functions to control an Instance:

 - [version](#singularity-version): control the instance command subgroup
 - [Shell](#shell) gives you an interactive python shell with a client
 - [Start](#create-an-instance) create a Singularity instance!
 - [Commands](#commands) how to interact with your instance (run, exec)
 - [Stop](#stop) stop the instance
 - [List](#list) list running Instances
 - [Stopall](#stop-all) stop all instances

Along with the above, there are a few client commands that will give you a list
of instances. While this listing doesn't directly link to finding an Instance that you
have created, you can find based on the name (shown later in the documentation).

<hr>

## Singularity Version
After Singularity 3.0, the instances command subgroup changed so that the original
call to interact with instances might have looked like "instances.list". After 3.0,
the [instances subgroup](https://github.com/sylabs/singularity/blob/master/CHANGELOG.md#v300---20181008)
changed to be of the format "instances list." Singularity Python determines this 
automatically by looking at your Singularity version, however if you want to control
the final command that is used (for one reason or another) you can also export
the environment variable:

```bash
export SPYTHON_SINGULARITY_VERSION=2.6
```

Would change behavior of the client for Singularity instances. This currently
only has this changed behavior for the instances subgroup.

## Shell
All of the commands below start with creating an spython client:

```bash
from spython.main import Client
```

but if you want, you can skip this step with the spython shell, which basically
loads it for you!

```bash
$ spython shell

Python 3.6.4 |Anaconda custom (64-bit)| (default, Jan 16 2018, 18:10:19) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client
Out[1]: [singularity-python]
```

You will be able to interact with instances via the Client, discussed in
the following sections.

<hr>

## Create an Instance

Running this command is equivalent to creating an instance from the 
command line, meaning that we "start" it. This means that an image is required.
Let's say that we have a local image, `ubuntu.simg`

```python
$ from spython.main import Client
$ myinstance = Client.instance('ubuntu.simg')
```

Optionally you can define other arguments! Just specify them as options. You can
split options into a list, where each entry is either a single flag, or a flag 
that is also given a value (the following item in the list). Below, let's create
some trivial directory, and try creating arguments to bind it to `/opt` in the instance.

```python
# This is on the host, not from within Python
mkdir -p /tmp/colors
echo "red orange yellow green blue violet pancake" >> /tmp/colors/rainbow.txt
```

Now we can bind this to `/opt` in our container.

```python
from spython.main import Client
options = ["--bind", "/tmp/colors:/opt"]
myinstance = Client.instance('ubuntu.simg', options=options)
```

You can check the options that were given to the instance:

```bash
$ myinstance.options
['--bind', '/tmp:/opt']
```

You can also check the entire command, which is saved with the instance object.


```bash
$ myinstance.cmd

['singularity',
 'instance.start',
 '--bind',
 '/tmp/colors:/opt',
 'spython/ubuntu.simg',
 'lovable_poo_3785']
```

Cool!

To check the bind, let's next learn how to interact with our instances.

<hr>


## Commands
Let's use the instance we created above, and try an exec command to see
if we successfully bound our `/tmp` to `/opt`. If you don't have the instance,
remember that you can ask for it by name:

```python
$ from spython.main import Client
$ myinstance = Client.instances('lovable_poo_3785', quiet=True)

myinstance
instance://lovable_poo_3785
```

Now let's list the contents of `/tmp/colors`

```bash
contents = Client.execute(myinstance,["ls","/tmp/colors"])

contents
$ 'rainbow.txt\n'
```

The same is true for run, and you can use the same arguments to bind, etc. as
you would for the client's [main commands](https://singularityhub.github.io/singularity-cli/commands#run).


## Stop
Instances have two states, alive (after started), and then dead of course.
To stop your instance, just stop it.

```bash
$ from spython.main import Client
$ myinstance = Client.instances('lovable_poo_3785', quiet=True)
$ myinstance.stop()

# This is the return code
0

$ Client.instances('lovable_poo_3785')
No instances found.
```

He's really gone!


### Stop All
If you want to stop all instances, that command is on the level of the main client
(it wouldn't make sense to have it associated with a single instance!)

```
from spython.main import Client
$ Client.instance_stopall()

# Return code
0

# Confirm no instances
$ Client.instances()
No instances found.


### List

First, to list running instances, here is what you see when there aren't any:

```bash
from spython.main import Client
Client.instances()
No instances found.
```

#### List (Instance Object)
The default listing will return a list of instance objects:

```python
$ instances = Client.instances()
DAEMON NAME      PID      CONTAINER IMAGE
blue_latke_2291  22472    /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg
creamy_train_2570 23162    /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg
```

If you don't want to see the Table printed, set `quiet=True` to prevent this.

```bash
instances = Client.instances(return_json=False, quiet=True)
```

If you look at the output, you have a list of instances:

```bash
$ instances
$ [instance://blue_latke_2291, instance://creamy_train_2570]
```

If you inspect one, you can get it's pid, it's name, associated container, and
some other useful things:

```bash
$ myinstance = instances.pop(0)

$ myinstance
instance://blue_latke_2291

$ myinstance.pid
'22472'

$ myinstance.name
'blue_latke_2291'

$ myinstance.get_uri()
'instance://blue_latke_2291'

$ myinstance._image
'/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg'
```

We explicitly don't have a "status" field because by way of existing, it's status
is started. If the status were stopped, you wouldn't find it.


#### List (Json)
If instances are found, a list is returned! The list is of json objects, each
with a daemon name, pid, and associted container image.

```bash
$ instances = Client.instances(return_json=True)
DAEMON NAME      PID      CONTAINER IMAGE
creamy           30859    /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg
tart_hippo_4068  1743     /home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg
```

Here is the json result:

```python
$ instances

[{'container_image': '/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg',
  'daemon_name': 'creamy',
  'pid': '30859'},
 {'container_image': '/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg',
  'daemon_name': 'tart_hippo_4068',
  'pid': '1743'}]
```


#### List (Single)
If you provide a specific instance name, this is akin to searching running instances
for it. The match is done based on name. For example, here we retrieve the instance
called `creamy`:

```python
$ Client.instances(name='creamy', quiet=True)
[{'container_image': '/home/vanessa/spython/ubuntu.simg',
  'daemon_name': 'creamy',
  'pid': '15051'}]
```

If you ask to return an object (discussed further in the next section) 
you can inspect it! For example:

```python
$ creamy = Client.instances(name='creamy', return_json=False,  quiet=True)
[instance://creamy]
```

You can then inspect things like the pid, and original container:

```python
$ creamy.pid
'15051'

$ creamy.name
'creamy'

$ creamy._image
'/home/vanessa/Documents/Dropbox/Code/sregistry/singularity-cli/spython/ubuntu.simg'

$ creamy.get_uri()
`instance://creamy`
```

It follows that if you search for a name that _doesn't_ exist, you won't find any
instances.


```python
$ Client.instances(name='creamier', quiet=True)
No instances found.
```

#### Logs

If you are running Singularity 3.5 or later, the instance logs (error and output)
should be programatically available, and you can return them via these functions:

```bash
logs = creamy.error_logs()
logs = creamy.output_logs()
```

To print them to the screen, set print_logs to True:

```bash
logs = creamy.error_logs(print_logs=True)
```

<div>
    <a href="/singularity-cli/commands"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/singularity-cli/commands-oci"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
