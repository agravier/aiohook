import asyncio
import importlib
import sys
from collections import deque

import aiofile
import aiohook

from textproc.pluginspecs import tokenize, transform_token


OES = object()


async def token_producer(out_q: asyncio.Queue):
    async with aiofile.AIOFile(sys.argv[2], 'rb') as f:
        async for token in tokenize(f):
            await out_q.put(token)
    await out_q.put(OES)


async def token_consumer(in_q: asyncio.Queue):
    async with aiofile.AIOFile(sys.argv[3], 'wb') as f:
        write = aiofile.Writer(f)
        eos = False
        while not eos:
            tokens = deque([await in_q.get()])
            while not in_q.empty():
                token = await in_q.get()
                tokens.append(token)
            if tokens[-1] is OES:
                eos = True
                tokens.pop()
            if tokens:
                transform_tasks = [transform_token(t) for t in tokens]
                transformed = await asyncio.gather(*transform_tasks)
                await write(b''.join(transformed))
            in_q.task_done()
        await f.fsync()


async def main():
    q = asyncio.Queue(maxsize=1000)
    await asyncio.gather(
        asyncio.ensure_future(token_producer(q)),
        asyncio.ensure_future(token_consumer(q)))


def cli():
    if len(sys.argv) != 4:
        print('Usage: process_text PLUGIN_MODULE IN_FILE OUT_FILE',
              file=sys.stderr)
        exit(1)
    aiohook.register(importlib.import_module(sys.argv[1]))
    asyncio.run(main())


if __name__ == "__main__":
    cli()
