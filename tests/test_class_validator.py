import unittest
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from classvalidator import validate


@dataclass
class SomeClass:
    one: str
    two: int
    three: float
    four: bytes
    five: Any
    six: List[str]
    seven: Dict[str, int]
    eight: Union[float, int]
    nine: Optional[Dict[str, int]]
    ten: Optional[Tuple[str, int, str]]


class TestClassValidator(unittest.TestCase):
    def setUp(self):
        # instantiate with valid values
        self.instance = SomeClass('value one', 22, 22.90, b'red', True, ['1', '67'],
                                  {'red': 90}, 90, {}, ('blue', 89, 'you'))

    def test_primitive_types(self):
        validate(self.instance)

        with self.assertRaises(TypeError):
            self.instance.two = 'should be an int'
            validate(self.instance)
        self.instance.two = 30
        validate(self.instance)

        with self.assertRaises(TypeError):
            # should be int not float
            self.instance.two = 89.9
            validate(self.instance)
        self.instance.two = 30
        validate(self.instance)

        with self.assertRaises(TypeError):
            self.instance.four = 'should be bytes'
            validate(self.instance)
        self.instance.four = b'should be bytes'
        validate(self.instance)

    def test_union_types(self):
        validate(self.instance)

        with self.assertRaises(TypeError):
            self.instance.eight = 'should be an int or float'
            validate(self.instance)

        self.instance.eight = 30
        validate(self.instance)

        self.instance.eight = 30.10
        validate(self.instance)

    def test_any_type(self):
        validate(self.instance)

        self.instance.five = 'as string'
        validate(self.instance)

        self.instance.five = b'as bytes'
        validate(self.instance)

        self.instance.five = 90.6
        validate(self.instance)

    def test_compund_types(self):
        validate(self.instance)
        with self.assertRaises(TypeError):
            # should be list not tuple
            self.instance.six = (2, 8)
            validate(self.instance)

        self.instance.six = ['list of string']
        validate(self.instance)

        with self.assertRaises(TypeError):
            # should be a dict not tuple
            self.instance.seven = (2, 8)
            validate(self.instance)

        self.instance.seven = {'red': 90}
        validate(self.instance)

        with self.assertRaises(TypeError):
            # should be tuple not list
            self.instance.ten = [2, 8, 90]
            validate(self.instance)

        self.instance.ten = ('blue', 89, 'you')
        validate(self.instance)
    
    def test_child_element_types(self):
        validate(self.instance)
        with self.assertRaises(TypeError):
            # should be list of string, not numbers
            self.instance.six = [2, 8]
            validate(self.instance)

        self.instance.six = ['list', 'of string']
        validate(self.instance)

        with self.assertRaises(TypeError):
            # should be tuple[str, int, str] not tuple[int, int, int]
            self.instance.ten = (2, 8, 90)
            validate(self.instance)

        self.instance.ten = ('blue', 89, 'you')
        validate(self.instance)

    def test_disallow_none(self):
        validate(self.instance)

        # None is allowed since it's Optional[Tuple]
        self.instance.ten = None
        validate(self.instance)
        with self.assertRaises(TypeError):
            # None should not be allowed when explicitly disallowed
            validate(self.instance, disallow_none=True)


if __name__ == '__main__':
    unittest.main()
