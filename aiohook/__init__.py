import functools
import inspect
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable, TypeVar, cast, NewType, Dict, Set, Iterator

from aiohook.type_inference import infer_type, ObjectType

ATTR_MARKER = '_aiohook_attributes'
HOOK_SPEC_REF_KEY = 'hook_spec_ref'

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)


_hookable_types: Set[ObjectType] = {
    ObjectType.sync_method,
    ObjectType.async_method,
    ObjectType.sync_function,
    ObjectType.async_function,
    ObjectType.sync_generator_method,
    ObjectType.async_generator_method,
    ObjectType.sync_generator_function,
    ObjectType.async_generator_function}


class AIOHookError(Exception):
    pass


class Singleton(type):
    """A metaclass for singleton objects."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


SpecRef = NewType('SpecRef', str)

ImplRef = NewType('ImplRef', Callable)


@dataclass
class Hook:
    typ: ObjectType
    impl_ref: ImplRef


class PluginRegistry(metaclass=Singleton):

    def __init__(self) -> None:
        self.all_spec_refs: Set[SpecRef] = set()
        self.ref_to_impl: Dict[SpecRef, Hook] = {}

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}({self.ref_to_impl})'

    def declare_hook_spec(self, spec_ref: SpecRef):
        self.all_spec_refs.add(spec_ref)

    def register_hook_impl(self, ref: SpecRef, fn_or_coro):
        if ref in self.ref_to_impl:
            if self.ref_to_impl[ref].impl_ref == fn_or_coro:
                return
            raise AIOHookError(f'Another plugin is already registered for '
                               f'{ref}: ({self.ref_to_impl[ref]})')
        self.ref_to_impl[ref] = Hook(typ=infer_type(fn_or_coro),
                                     impl_ref=fn_or_coro)

    @property
    def hook_specs_without_plugin_impl(self) -> Set[SpecRef]:
        return self.all_spec_refs - set(self.ref_to_impl)

    @property
    def plugin_impl_without_hook_specs(self) -> Set[SpecRef]:
        return set(self.ref_to_impl) - self.all_spec_refs


def spec(fn: F) -> F:
    spec_ref = SpecRef(f'{inspect.getmodule(fn).__name__}.{fn.__qualname__}')
    PluginRegistry().declare_hook_spec(SpecRef(spec_ref))
    object_type = infer_type(fn)
    if object_type is ObjectType.sync_function:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                impl: Hook = PluginRegistry().ref_to_impl[spec_ref]
            except KeyError:
                print(f'Calling default impl of {spec_ref}')
                return fn(*args, **kwargs)
            else:
                print(f'Calling plugin impl of {spec_ref}: {impl.impl_ref}')
                return impl.impl_ref(*args, **kwargs)
        return cast(F, wrapper)
    elif object_type == ObjectType.async_function:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                impl: Hook = PluginRegistry().ref_to_impl[spec_ref]
            except KeyError:
                print(f'Calling default impl of {spec_ref}')
                return await fn(*args, **kwargs)
            else:
                print(f'Calling plugin impl of {spec_ref}: {impl.impl_ref}')
                return await impl.impl_ref(*args, **kwargs)
        return cast(F, wrapper)
    elif object_type == ObjectType.async_generator_function:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                impl: Hook = PluginRegistry().ref_to_impl[spec_ref]
            except KeyError:
                print(f'Calling default impl of {spec_ref}')
                async for res in fn(*args, **kwargs):
                    yield res
            else:
                print(f'Calling plugin impl of {spec_ref}: {impl.impl_ref}')
                async for res in impl.impl_ref(*args, **kwargs):
                    yield res

        return cast(F, wrapper)
    else:
        raise NotImplementedError(object_type.name)


def impl(spec_ref: str) -> Callable[[F], F]:
    spec_ref = SpecRef(spec_ref)

    def mark_function(func: F) -> F:
        PluginRegistry().register_hook_impl(spec_ref, func)
        setattr(func, ATTR_MARKER, {HOOK_SPEC_REF_KEY: spec_ref})
        return func

    return mark_function


def register(obj):
    print(f"registering {obj}")
    typ: ObjectType = infer_type(obj)
    if typ == ObjectType.module or typ == ObjectType.instance:
        all_hooks = find_hook_implementations(obj)
        for hook in all_hooks:
            register(hook)
    elif typ in _hookable_types:
        hook_marker = get_hook_marker(obj)
        if hook_marker:
            try:
                spec_ref = SpecRef(hook_marker[HOOK_SPEC_REF_KEY])
            except KeyError:
                print('Missing spec ref key in hook marker. This may be a bug.')
                return
            PluginRegistry().register_hook_impl(spec_ref, obj)
    else:
        raise TypeError(
            f"The plugin registration function got passed what seems to be a "
            f"{typ.name}, but it expects a module or an instance of a class "
            f"containing decorated hook implementations, or direct references "
            f"to decorated hook implementations.")


def is_hookable(elem: Any) -> bool:
    return infer_type(elem) in _hookable_types


def get_hook_marker(elem: Any) -> Dict:
    try:
        return getattr(elem, ATTR_MARKER, {})
    except:
        return {}


def find_hook_implementations(obj: ModuleType) -> Iterator[Any]:
    for element_str in dir(obj):
        element = getattr(obj, element_str)
        if not is_hookable(element):
            continue
        hook_marker = get_hook_marker(element)
        if hook_marker:
            yield element

