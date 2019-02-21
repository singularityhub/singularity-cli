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
 - fixing bug with instances list, name not taken into account (0.0.51)
 - additional of args to instance start commands (0.0.50)
 - continued lines should not be split in docker.py recipe parser (_setup) (0.0.49)
 - COPY command should honor src src dest (and not reverse) (0.0.48)
 - adding support for instance list (0.0.47)
 - ENV variables in Dockerfile can be empty (like unsetting) (0.0.46)
 - COPY can handle multiple sources to one destination for Dockerfile parser (0.0.45)
 - Adding DockerRecipe, SingularityRecipe "load" action to load file
 - issue #64 bug with hanging instances (0.0.44)
 - flexible error printing given command to terminal fails (0.0.43)
 - adding name_by_commit and name_by_hash to pull (0.0.42)
 - adding nvidia flag as nv argument (with default False) to run/exec (0.0.41)
 - fixing bug in shell.py, cli should be client (0.0.40)
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
