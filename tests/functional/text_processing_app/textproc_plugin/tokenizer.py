from typing import AsyncIterator, Tuple, TypeVar

import aiohook
import aiofile
from textproc_plugin.settings import CHUNK_SIZE_IN_BYTES

T = TypeVar('T')


async def async_enumerate(seq: AsyncIterator[T], start=0) \
        -> AsyncIterator[Tuple[int, T]]:
    """Asynchronously enumerate an async iterator from a given start value"""
    n = start
    async for elem in seq:
        yield n, elem
        n += 1


@aiohook.impl('textproc.pluginspecs.tokenize')
async def tokenize_in_fixed_chunks(f: aiofile.AIOFile) \
        -> AsyncIterator[Tuple[int, bytes]]:
    reader = aiofile.Reader(f, chunk_size=CHUNK_SIZE_IN_BYTES)
    async for i, chunk in async_enumerate(reader):
        yield i, chunk
