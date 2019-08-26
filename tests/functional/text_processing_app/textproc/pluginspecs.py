from typing import Optional, AsyncIterator, TypeVar
import aiofile
import aiohook


T = TypeVar('T')
U = TypeVar('U')


@aiohook.spec
async def tokenize(f: aiofile.AIOFile) -> AsyncIterator[T]:
    """Split string of characters into individual tokens."""
    # workaround for python's type system inability to declare a generator
    # function without a body with a 'yield' somewhere
    yield


@aiohook.spec
async def transform_token(word: T) -> Optional[U]:
    """Preprocess each raw token, for instance as a normalization step."""
