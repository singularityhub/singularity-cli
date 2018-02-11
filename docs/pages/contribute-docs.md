---
layout: default
title: Contribute to Singularity Python Client Documentation
pdf: true
permalink: /contribute-docs
toc: false
---

# Singularity Python API Documentation

The documentation is served in the Github pages site served in the docs folder.
If you clone the repo, cd into this folder, and then install (and run) Jekyll you
can usually get started working on the documentation.


## Dependencies
Initially (on OS X), you will need to setup [Brew](http://brew.sh/) which is a package manager for OS X and [Git](https://git-scm.com/). To install Brew and Git, run the following commands:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
```
If you are on Debian/Ubuntu, then you can easily install git with `apt-get`

```bash
apt-get update && apt-get install -y git
```

### Fork the Repository
To contribute to the web based documentation, you should obtain a GitHub account and *fork* the <a href="https://github.com/singularityhub/singularity-cli/" target="_blank">Singularity Python</a> repository by clicking the *fork* button on the top right of the page. Once forked, you will want to clone the fork of the repo to your computer. Let's say my Github username is *vsoch*:

```bash
git clone https://github.com/vsoch/singularity-cli.git
cd singularity-cli
```

### Install Jekyll
You can also install Jekyll with brew.

```bash
brew install ruby
gem install jekyll
gem install bundler
bundle install
```
On Ubuntu I do a different method:

```
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
exec $SHELL
rbenv install 2.3.1
rbenv global 2.3.1
gem install bundler
rbenv rehash
ruby -v

# Rails
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs
gem install rails -v 4.2.6
rbenv rehash

# Jekyll
gem install jekyll
gem install github-pages
gem install jekyll-sass-converter

rbenv rehash
```

## Build and Serve
After you cd into the docs folder (the base of the site) you can see the site locally by running the server with jekyll:

```bash
cd docs/
bundle exec jekyll serve
```

or sometimes this works.

```
jekyll serve
```

And the site will be viewable at <a href="http://127.0.0.1:4000/singularity-cli/" target="_blank">http://127.0.0.1:4000/singularity-cli/</a>. You can edit the markdown files in various folders to see changes in your browser, and push to your fork and then pull request to make changes. If you have a minor change, you can also do a patch directly in your browser from Github.

<div>
    <a href="/singularity-cli/commands"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/singularity-cli"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
