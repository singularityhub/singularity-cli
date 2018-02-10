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

## Pyshell
If you want to jump right you, you can start a python shell (`pyshell`) to have a client ready to go!

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

In [1]: client.simage
Out[1]: docker://ubuntu
```

<div>
    <a href="/singularity-cli/d"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/sregistry-cli/client"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
