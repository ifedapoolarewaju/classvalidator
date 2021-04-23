# classvalidator

Classvalidator offers runtime type validation of `dataclasses.dataclass` instances using their type hint information.

## Installation

`pip install classvalidator`

## Usage

To use, simply import the `classvalidator.validate` function and call it on any dataclass instance you'd like to validate. The following is a simple example:

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from classvalidator import validate

@dataclass()
class SomeClass:
    some_atrr_one: str
    some_atrr_two: int
    some_atrr_three: List[int]

# valid instance
instance = SomeClass(some_atrr_one='value one', some_atrr_one=22, some_atrr_three=[1, 2])

# no errors
validate(instance)

# resetting some attributes to invalid types (aka make the instance invalid)
instance.some_atrr_two = 'should be an int, not string'

# TypeError will be thrown on validation
try:
    validate(instance)
except TypeError as e:
    print(e)
```

You can also validate iterables and their elemet types (e.g `List[str]`, `Tuple[str, str, int]`. Here's an example:

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from classvalidator import validate

@dataclass()
class SomeClass:
    some_atrribute: Tuple[int, str]

# valid instance
instance = SomeClass(some_atrribute=(10, 'some value'))

# no errors
validate(instance)

# resetting tuple elements to an invalid Tuple[int, int]
instance.some_atrribute = (10, 10)

# TypeError will be thrown on validation
try:
    validate(instance)
except TypeError as e:
    print(e)
```

## Limitations

- This library has only been tested on Python >= 3.72
- Only builtin python types are supported (i.e `bool, str, int, float, List, Tuple, Dict, Set`, etc.)
- Validation only happens for recognised types. Unrecognised types will be ignored without failure.
- Even though Dictionary types are validated, the `key-value` types are not validated
- For Tuples with `Elipsis`, the element types will not be validated
