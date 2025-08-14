# Api Starter

To run the project, Python version >= 12 is required.
I suggest you use pyenv.

## Setup

Create python environment:

```bash
    $ pyenv exec python -m venv .venv
```

Create a database using docker
```bash
    $ docker-componse up -d --build
```

Activate the python environment
```bash
    # Unix
    $ source .venv/bin/active
    
    # Windows
    $ source .venv/Scripts/active
    
    $ cd api
```

Setuptools should be installed in your environment by default, but if it is not, use
```bash
    $ pip install -r requirements.txt
```

Finally we can install our API. If you don't use make file, copy the command from file without '@'
```bash
    $ make dev_install
```

Once everything is installed, use initialize database. Basic user and task models will be created in the database
```bash
    $ make load_fixtures
```

Done, now you can run the API
```bash
    $ make dev_run
```

## Tests

To run the tests, follow the steps in the [Setup](#setup) section.

Then use command
```bash
    $ make test
```
