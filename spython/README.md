# Singularity Python Organization
This will briefly outline the content of the folders here.

## Main Functions

 - [main](main) holds the primary client functions to interact with Singularity (e.g., exec, run, pull), and the subfolders within represent command groups (e.g., instance, image) along with the base of the client ([base](main/base))
 - [image](image) is a class that represents and holds an image object, in the case that the user wants to initialize a client with an image.
 - [cli](cli): is the actual entry point that connects the user to the python API client from the command line. The user inputs are parsed, and then passed into functions from main.

## Supporting
 - [utils](utils) are various file and other utilities shared across submodules.
 - [logger](logger) includes functions for progress bars, and logging levels.
 - [tests](tests) are important for continuous integration, but likely overlooked.
