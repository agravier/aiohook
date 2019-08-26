from enum import Enum
import inspect
from typing import Any


def _type_field_of_object(obj: Any) -> int:
    """Create bitfield that allows differentiating modules, classes,
    functions (routines and unbound methods), bound methods, generator
    functions (and unbound generator functions), coroutine functions
    ("async functions"), and async generator functions."""
    bitfield = \
        inspect.isbuiltin(obj) * 2 ** 7 + \
        inspect.ismodule(obj) * 2 ** 6 + \
        inspect.isclass(obj) * 2 ** 5 + \
        inspect.ismethod(obj) * 2 ** 4 + \
        inspect.isroutine(obj) * 2 ** 3 + \
        inspect.iscoroutinefunction(obj) * 2 ** 2 + \
        inspect.isasyncgenfunction(obj) * 2 + \
        inspect.isgeneratorfunction(obj)
    return bitfield


class _A:
    """Sample dummy class used to construct the HookType bit field"""
    def sync_method(self, arg: int) -> int:
        return arg

    async def async_method(self, arg: int) -> int:
        return arg

    def sync_generator_method(self, arg: int) -> int:
        for x in range(arg):
            yield arg

    async def async_generator_method(self, arg: int) -> int:
        for x in range(arg):
            yield arg


_a = _A()


class ObjectType(Enum):
    other = -1
    module = _type_field_of_object(inspect)
    class_ = _type_field_of_object(_A)
    instance = _type_field_of_object(_a)
    builtin_function = _type_field_of_object(dir)
    sync_method = _type_field_of_object(_a.sync_method)
    async_method = _type_field_of_object(_a.async_method)
    sync_function = _type_field_of_object(_A.sync_method)
    async_function = _type_field_of_object(_A.async_method)
    sync_generator_method = _type_field_of_object(_a.sync_generator_method)
    async_generator_method = _type_field_of_object(_a.async_generator_method)
    sync_generator_function = _type_field_of_object(_A.sync_generator_method)
    async_generator_function = _type_field_of_object(_A.async_generator_method)


def infer_type(o: Any) -> ObjectType:
    try:
        return ObjectType(_type_field_of_object(o))
    except ValueError:
        return ObjectType.other