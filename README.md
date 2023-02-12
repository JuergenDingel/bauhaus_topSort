# Computing topological orderings with Bauhaus


## Summary

We use the Python library Bauhaus (https://bauhaus.readthedocs.io) to encode ordering (precedence, dependency) constraints and solve them, i.e., compute orderings that are consistent with the constraints. The main purpose is to provide another example of the use of Bauhaus. As a project in CISC 204 it would probably be too simple (we'll use the CISC 204 project template nonetheless). Note that none of the expected documents are provided. 


## To run things

### Building
```docker build -t cisc204 .```

### Running
```docker run -it -v $(pwd):/PROJECT cisc204```


## Structure
### General or provided
* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

### Custom code
* `run*.py`: Contains code to build the encoding, solve it, and output the result.
