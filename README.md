# Python SDK

Currently built for python 2.7

Requires an environment variable setup file. Example is in .env\_example

## Install
Copy files into your project, include and run.

The directory structure should look like this:

```
📂root directory
 └ main.py
 └📂flosdk
   └ flosdk.py
   └ __init__.py
```

## Running

Start by sourcing the environment variable file.

```
source .env
```

Then, implement flosdk in your python project, and test if it works:

```
import flosdk from flosdk
print flosdk.get_info()
```


Then run `main.py`: 
```
python main.py
```

## Debugging

Here are some usual errors that might be encountered:
