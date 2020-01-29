# CHANGELOG

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented by the pull requests that fixed them.
Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes (recipe or image file format?)
 - migration guidance (how to convert images?)
 - changed behaviour (recipe sections work differently)

The client here will eventually be released as "spython" (and eventually to
singularity on pypi), and the versions here will coincide with these releases.

## [master](https://github.com/singularityhub/singularity-cli/tree/master)
 - instance list includes ip address (0.0.76)
 - export lines aren't ignored from environment, but replaced (0.0.75)
 - instance logging functions for Singularity 3.5 and up (0.0.74)
 - add sudo_options option to spython.main.Client.build (0.0.73)
 - list of options and writable added to shell, execute, and run (0.0.72)
 - client is not honoring quiet for pull (0.0.71)
 - removing debugging line in pull (0.0.70)
 - adding quiet argument to build to override client (0.0.69)
 - adding additional options to build to support singularity-compose (0.0.68)
 - client should support shell (0.0.67)
 - adding test for entrypoint + cmd and fixing testing requirements (0.0.66)
 - fixing bug that inspect does not honor quiet (0.0.65)
 - refactor recipe parsers, writers, and base (0.0.64)
   - paths for files, add, copy, will not be expanded as it adds hardcoded paths
 - oci state fixes and added Client.version_info() (0.0.63)
 - fix crash in some error conditions (0.0.62)
   - more OCI commands accept sudo parameter
 - working directory, the last one defined, should be added to runscript (0.0.61)
 - adding deprecation message for image.export (0.0.60)
   - adding --force option to build
 - fixing warning for files, only relevant for sources (0.0.59)
 - deprecating pulling by commit or hash, not supported for Singularity (0.0.58)
   - export command added back, points to build given Singularity 3.x+
 - print but with logger, should be println (0.0.57)
 - Fixing bug with instance not having name when not started (0.0.56)
   - instance start has been moved to non-private
 - Added ability for exec and run to return the full output and message (0.0.55)
  - By default, oci commands (pause, resume, kill) return the return value
 - Added support and tests for OCI image command group (0.0.54)
   - client now has version() function to call get_singularity_version
   - added return_result (boolean) to client run_command function.
 - adding testing for 3.1.0 with Singularity Orbs (0.0.53)
   - inspect returns parsed json on success, or full message / return code otherwise
 - instance stop all missing check for Singularity V3.+ (0.0.52)
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
