---
layout: default
title: Installation
pdf: true
permalink: /install
toc: false
---

# Installation Local

To install from the Github repository:

```
git clone https://www.github.com/singularityhub/singularity-cli.git
cd singularity-cli
python setup.py install
```

And you can also install from pip:

```
# Client and Database
pip install spython
```


# Singularity
You can also use our Singularity image provided, each directly from Singularity
Hub, or via building on your own. To build a singularity container

```
sudo singularity build spython Singularity
```
