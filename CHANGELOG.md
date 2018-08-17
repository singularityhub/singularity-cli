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
 - remove uri function should only right strip to support relative paths (0.0.39)
 - adjusting container build to use correct Github branch (vault/release-2.5)
 - adding support and documentation for container instances (0.0.38)
 - fixing bug with recipe Dockerfile conversion (0.0.37)
 - typo in pypi PACKAGE_URL (0.0.36)
 - respecting Client "quiet" attribute in run_command  (0.0.34/0.0.35)
 - adding missing import of tempfile in image.export (0.0.33)
 - bug with Client.version() (0.0.32)
 - fixing bugs with import, export, image commands (0.0.31)
 - adding tests for client (0.0.30)
 - bug in Dockerfile fromHeader variable fix (0.0.29)
 - Dockerfile from "as level" removed (0.0.28)
 - fixed ENV parser to handle statements like A=B C=D
 - adding ability to stream command executed to console (0.0.25)
 - fixing import bug with recipe parsers in python 2.7 (0.0.24)
 - addition of docker and singularity recipe parsers (0.0.22)
 - adding bind argument to exec and run (0.0.21)
 - generating basic api documentation (sphinx) (0.0.2)
 - adding changelog, and original code for client  (0.0.1)
