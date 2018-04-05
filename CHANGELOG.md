# CHANGELOG

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented by the pull requests that fixed them.
Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes (recipe file format? image file format?)
 - migration guidance (how to convert images?)
 - changed behaviour (recipe sections work differently)

The client here will eventually be released as "spython" (and eventually to
singularity on pypi), and the versions here will coincide with these releases.

## [master](https://github.com/singularityhub/singularity-cli/tree/master)
 - fixing import bug with recipe parsers in python 2.7 (0.0.24)
 - addition of docker and singularity recipe parsers (0.0.22)
 - adding bind argument to exec and run (0.0.21)
 - generating basic api documentation (sphinx) (0.0.2)
 - adding changelog, and original code for client  (0.0.1)
