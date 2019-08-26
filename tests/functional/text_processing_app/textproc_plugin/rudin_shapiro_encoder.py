"""Encode data using a non-cryptographic cypher based on the Rudin-Sharpio
integer sequence"""
import functools
from typing import AsyncIterator, Tuple, TypeVar

import aiofile
import aiohook
import textproc_plugin.rudin_sharpio_seq as rss

CYPHER_KEY = 987149975134
CHUNK_SIZE_IN_BYTES = 16
CHUNK_SIZE_IN_BITS = CHUNK_SIZE_IN_BYTES * 8

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
        -> AsyncIterator[Tuple[int, int]]:
    reader = aiofile.Reader(f, chunk_size=CHUNK_SIZE_IN_BYTES)
    async for i, chunk in async_enumerate(reader):
        yield i, int.from_bytes(chunk, byteorder='big', signed=False)


@aiohook.impl('textproc.pluginspecs.transform_token')
async def encode(indexed_token: Tuple[int, int]) -> bytes:
    idx, token = indexed_token
    bit_idx = CYPHER_KEY + idx * CHUNK_SIZE_IN_BITS
    mask = functools.reduce(
        lambda n, b: n << 1 | b,
        (rss.b(bit_idx + i) for i in range(CHUNK_SIZE_IN_BITS)))
    result = token ^ mask
    return result.to_bytes(
        length=CHUNK_SIZE_IN_BYTES, byteorder='big', signed=False)

