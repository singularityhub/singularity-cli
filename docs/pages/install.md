---
layout: default
title: Installation
pdf: true
permalink: /install
toc: false
---

# Installation Local
You need `python3` and `pip` in order to use this API.

To install from the Github repository:

```bash
git clone https://www.github.com/singularityhub/singularity-cli.git
cd singularity-cli
python setup.py install
```

And you can also install from pip:

```bash
# Client and Database
pip install spython
```


# Singularity
You can also use our Singularity image provided, each directly from Singularity
Hub, or via building on your own. To build a singularity container

```
sudo singularity build spython Singularity
```

<div>
    <a href="/singularity-cli/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/singularity-cli/commands"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
