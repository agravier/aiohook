# aiohook – simple plugins for asyncio, trio and curio

*aiohooks* is a small library meant to help implementing a plugin system in 
Python 3.7+ asynchronous applications developed with an _anyio_-compatible 
library. It can also be used to set up synchronous function hooks.

## Quickstart

- Declare the signature of the hook coroutine by decorating a dummy `def` or
`async def` (without implementation, or with a default one) with `aiohook.spec`.
- `await` the dummy coroutine where you would want the plugin one to be called.
- Implement the dummy coros in a separate module or class and decorate them with 
`aiohook.impl('reference.to.dummy')`.
- Call `aiohook.register(reference)` to register the decorated implementations 
in `reference` (object instance or module). 
- Non-implemented hooks result in the default implementation being called.
- Registering multiple implementations of the same hook raises an exception.

## Basic usage

In this story, your name is Wallace, you are implementing an awesome async
application accepting plugins. Your user, Gromit, wants to make use of your
plugin system to inject his custom parsing logic.

### Application designer

You must first define the signature of each hook function, for
instance in a separate _pluginspecs.py_ file:

```python
from typing import Sequence, Optional
import aiohook

@aiohook.spec
async def tokenize(sentence: str) -> AsyncIterator[str]:
    # Describe the purpose of the hook, arguments etc in the docstring
    """Split string of characters into individual tokens."""
    # workaround for python's type system inability to declare a generator
    # function without a body with a 'yield' somewhere
    yield

@aiohook.spec
async def transform_token(word: str) -> Optional[str]:
    """Preprocess each raw token, for instance as a normalization step."""
```

In your application code, you then call your spec'ed out functions as if they had 
already been implemented:

```python
import sys, asyncio, importlib, aiohook
from pluginspecs import tokenize, transform_token

async def main():
    with open(sys.argv[1], 'r') as f:
        source = f.read()
    async for token in tokenize(source):
        transformed = await transform_token(token)
        print(transformed, end='')

if __name__ == '__main__':
    aiohook.register(importlib.import_module(sys.argv[1]))
    asyncio.run(main())
``` 

### Plugin developer




## Development

Two requirements files are used to describe the development setup:

- The requirements.txt file describes a working development environment with all 
pinned dependencies. 
- The requirements-base.txt file contains the direct unpinned dependencies only
necessary for a full development environment.

### Step-by-step guide to set up a development environment

This assumes that [pyenv](https://github.com/pyenv/pyenv) and pyenv-virtualenv 
are installed, and the OS is somehow Unix-like. Commands are executed from the
root of the repo.

```shell script
pyenv install 3.7.4
pyenv virtualenv 3.7.4 aiohook-dev-3.7.4 
pyenv activate aiohook-dev-3.7.4
```

To work on the main library, it is best to just pip install it as an editable 
package, and install the rest of the dev requirements:

```shell script
pip install -e .
pip install -r requirements.txt
```

To work on one of the functional test applications under _tests/functional_, it
is useful to also install it in editable mode in the same environment:

```shell script
pip install -e tests/functional/text_processing_app
# Try it out
process_text textproc_plugin requirements.txt requirements-transformed.txt
```

### Testing with coverage 

```shell script
pytest --cov=aiohook tests/
```
