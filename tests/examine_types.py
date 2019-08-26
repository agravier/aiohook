import asyncio
import inspect


def reveal_type(o):
    print(f'\n{o} (typed as {type(o)}):')
    for s, f in [
        ("is a module", inspect.ismodule),
        ("is a class", inspect.isclass),
        ("is a method", inspect.ismethod),
        ("is a function", inspect.isfunction),
        ("is a routine", inspect.isroutine),
        ("is awaitable", inspect.isawaitable),
        ("is an async gen function", inspect.isasyncgenfunction),
        ("is an async gen", inspect.isasyncgen),
        ("is a generator function", inspect.isgeneratorfunction),
        ("is a generator", inspect.isgenerator),
        ("is a coroutine function", inspect.iscoroutinefunction),
        ("is a coroutine", inspect.iscoroutine),
    ]:
        print(f' - {s:>25} → {"☑ YES" if f(o) else "☐ no"}')


class A:
    def sync_method(self, arg: int) -> int:
        return arg

    async def async_method(self, arg: int) -> int:
        await asyncio.sleep(1)
        return arg

    def __call__(self, *args, **kwargs):
        print(f'{args}, {kwargs}')


reveal_type(inspect)

reveal_type(A)

reveal_type(A())

reveal_type(A.sync_method)

reveal_type(A().sync_method)

reveal_type(A.async_method)

reveal_type(A().async_method)


def sync_function(arg: int) -> int:
    return arg


async def async_function(arg: int) -> int:
    return arg


reveal_type(sync_function)

reveal_type(async_function)


def sync_generator_function(arg: int) -> int:
    for x in range(arg):
        yield arg


async def async_generator_function(arg: int) -> int:
    await asyncio.sleep(1)
    for x in range(arg):
        yield arg


reveal_type(sync_generator_function)

reveal_type(async_generator_function)
