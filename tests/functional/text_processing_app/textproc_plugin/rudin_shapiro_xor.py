"""Encode data using a non-cryptographic cypher based on the Rudin-Sharpio
integer sequence"""
import functools
from typing import Tuple

import aiohook
import textproc_plugin.rudin_sharpio_seq as rss

from textproc_plugin.settings import CHUNK_SIZE_IN_BITS, CYPHER_KEY


@aiohook.impl('textproc.pluginspecs.transform_token')
async def encode(indexed_token: Tuple[int, bytes]) -> bytes:
    idx, token = indexed_token
    bit_idx = CYPHER_KEY + idx * CHUNK_SIZE_IN_BITS
    mask_int = functools.reduce(
        lambda n, b: n << 1 | b,
        (rss.b(bit_idx + i) for i in range(len(token)*8)))
    mask = mask_int.to_bytes(len(token), byteorder='big', signed=False)
    result = bytes(a ^ b for (a, b) in zip(token, mask))
    return result
