# aiohook – simple plugins for asyncio, trio and curio

*aiohooks* is a small library meant to help implementing a plugin system in 
Python 3.7+ asynchronous applications developed with an _anyio_-compatible 
library.

## Quickstart

- Declare the signature of the hook coroutine by decorating a dummy `def`
(without implementation, or with a default one) with `aiohook.spec`.
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
async def tokenize(sentence: str) -> Sequence[str]:
    # Describe the purpose of the hook, arguments etc in the docstring
    """Split string of characters into individual tokens."""
    # No implementation here, this is just a function spec

@aiohook.spec
async def transform_token(word: str) -> Optional[str]:
    """Preprocess each raw token, for instance as a normalization step."""
```

In your application code, you then call your spec'ed out functions as if they had 
already been implemented:

```python
import sys
from pluginspecs import tokenize, transform_token

with open(sys.argv[1], 'r') as f:
    
``` 

### Plugin developer




## Development

Two requirements files are used to describe the development setup:

- The requirements.txt file describes a working development environment with all 
pinned dependencies. 
- The requirements-base.txt file contains the direct unpinned dependencies only.

### Testing with coverage 

```shell script
pytest --cov=aiohook tests/
```
