import builtins
from typing import Any, List, Tuple, get_type_hints

from typing_inspect import get_args, get_origin, is_union_type

_BUILTINS = set(dir(builtins))


def _is_builtin(type_) -> bool:
    #  NoneType is not part of builtins but we need it to account for "Optional"
    return getattr(type_, '__name__', None) in _BUILTINS or type_ is type(None)


def _get_root_type(type_):
    root_type = type_
    if not _is_builtin(root_type):
        root_type = get_origin(type_)
    return root_type


def _can_validate_children(child_args, value) -> bool:
    valid_type = isinstance(child_args, tuple) and isinstance(value, (list, tuple, set))
    return valid_type and len(child_args) in {1, len(value)}


def _validation_error(attr: str, value: Any) -> TypeError:
    return TypeError(f'invalid value type for attribute "{attr}" got {type(value)}')


def _validate(value: Any, attr: str, root_type, type_args):
    if not isinstance(value, root_type):
        raise _validation_error(attr, value)

    # in the case of List[str], Set[int], Tuple[str, int]
    # we need to vaidate their child elements (i.e args)
    if _can_validate_children(type_args, value):
        for idx, child_value in enumerate(value):
            index = idx if len(type_args) > 1 else 0
            child_type = _get_root_type(type_args[index])
            if _is_builtin(child_type):
                if not isinstance(child_value, child_type):
                    raise _validation_error(attr, value)


def validate(obj: Any, disallow_none=False) -> None:
    """Validates a Dataclass instance that its attribute values match the type hints
    specified. It raises a TypeError if the validation fails.
    :param obj: Any - The Dataclass instance whose fiedlds you want to validate
    :param disallow_none: Optional[bool] - if True, even when an attributes type hint is
        "Optional", it will fail the validation if its value is None.
    """
    type_hints = get_type_hints(obj)
    for attr, type_ in type_hints.items():
        value = getattr(obj, attr)
        if disallow_none and value is None:
            raise TypeError(f'atrribute {attr} cannot be "None"')

        args = get_args(type_)
        root_type = _get_root_type(type_)
        if _is_builtin(root_type):
            _validate(value, attr, root_type, args)
            continue

        if is_union_type(root_type):
            root_types: List[Tuple] = []
            for sub_type in args:
                sub_type_args = get_args(sub_type)
                root_type = _get_root_type(sub_type)
                if not _is_builtin(root_type):
                    break

                root_types.append((root_type, sub_type_args))
            
            if len(root_types) == len(args):
                failure_count = 0
                for root_type, type_args in root_types:
                    try:
                        _validate(value, attr, root_type, type_args)
                        break
                    except TypeError:
                        failure_count += 1

                if failure_count == len(root_types):
                    raise _validation_error(attr, value)

                continue
