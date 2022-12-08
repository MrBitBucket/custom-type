# custom-type
Simple test module for abi3 testing based on

  https://docs.python.org/3.7/extending/newtypes_tutorial.html#the-basics

Has a setup.py based on 

  https://github.com/joerick/python-abi3-package-sample


An evironment variable switches between standard build and abi3 compatible.

This stadard build works

```
ABI3_WHEEL=0 pip wheel -w dist .
```

but this which attempts to use an abi3 build fails.

```
ABI3_WHEEL=1 pip wheel -w dist .
```
