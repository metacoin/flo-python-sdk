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

## Structure

The FLO SDK should include all of the following:

1. RPC interface connecting to a local or remote FLO RPC daemon.
2. Cross-platform (sqlite3 or NoSQL) database to store transaction data.
3. Web-facing API for database.
4. Client interface connecting to web-facing database APIs.

Nice to have:
1. Alexandria / OIP API functions.
2. Flotorizer / SharedSecret functions. 
3. Ability to connect to a pre-funded remote RPC.
4. SSL for the connection between the local client and server.

### RPC interface connecting to a local or remote FLO RPC daemon

This should include every RPC call available in the FLO RPC list. It should also handle all errors that could be returned by the FLO RPC. 

### Cross-platform sqlite3 or NoSQL database to store transaction data

The SDK should have an option to store transaction data in a local database. Optionally, it should have "plugins" to recognize different protocols popular on the network.

### Web-facing API for database

The database should be accessible via a web-facing API. This API, if on a web-facing server, should host data for remote nodes connecting to it. Otherwise it will have its own local API over the local network as usual.

### Client SDK for connecting to web-facing database APIs

The client should be able to connect to a web-facing API to receive database information. This would be considered a "light" client -- one that doesn't have the blockchain or any database information -- it relies on an external (trusted 3rd party or self-hosted) server for data.

### Alexandria / OIP API functions

Alexandria and OIP functions should be exposed in the library to make it easy to build into the Alexandria platform.

### Flotorizer / SharedSecret functions

Same as above.

### Ability to connect to a pre-funded remote RPC

Some clients won't have funds or any way to get funds, but will still want to post things on the blockchain. There should be some process of acquiring a `funded key` from a web-facing server that allows authorized clients to post to the blockchain after authenticating with their `funded key`.

### SSL for the connection between the local client and server

The local client and server should have a secure tunnel to communicate with.

## Debugging

Here are some usual errors that might be encountered:

#### `Exception: HTTPConnectionPool Max retries exceeded`

This error, alongside `Failed to establish a new connection: [Errno 111] Connection refused`, usually means the FLO RPC cannot be found. Make sure the FLO RPC is still running.
```
Exception: HTTPConnectionPool(host='localhost', port=7313): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f6c029f2310>: Failed to establish a new connection: [Errno 111] Connection refused',))
```

