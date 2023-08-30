import unittest
from typing import Dict, Union
from decorator_validation.decorators import check_types
from decorator_validation.types import SkipTypeCheck
import logging


class TestConvertWith(unittest.TestCase):
    def test_correct_types_only_kwargs(self):
        @check_types
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(bar=3, message="some string", some_additional_info=dict())
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_only_args(self):
        @check_types
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(3, "some string", dict())
        except Exception as e:
            worked = False
            logging.error(e)
        self.assertEqual(worked, True)

    def test_correct_types_mix_args_kwargs(self):
        @check_types
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            worked = foo(
                3,
                some_additional_info=dict(),
                message="some string",
            )
        except Exception as e:
            logging.error(e)
        self.assertEqual(worked, True)

    def test_uncorrect_types(self):
        @check_types
        def foo(bar: int, message: str, some_additional_info: Dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_union_types(self):
        @check_types
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar=3.2, message="some string", some_additional_info=dict()))
            _ = foo(dict(bar=3, message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_skip_type_check(self):
        @check_types
        def foo(bar: Union[int, float], message: Union[str, bytes], some_additional_info: dict):
            return True

        try:
            _ = foo(dict(bar="also string", message=bytes("some bytes"), some_additional_info=dict()))
        except TypeError:
            worked = True
        else:
            worked = False
        self.assertEqual(worked, True)

    def test_cls_and_obj_stuff(self):
        class Test:
            @check_types
            def __init__(self, k: int):
                pass

            @classmethod
            @check_types
            def from_stuff(cls, k: int):
                pass

        Test(1)
        Test.from_stuff(1)

    def test_none(self):
        @check_types
        def none_test(a: Union[None, str] = None):
            print(a)

        none_test
        none_test(None)
        try:
            none_test(1)
            assert False
        except TypeError:
            assert True

    def test_notype(self):
        @check_types
        def foo(bar):
            print(bar)

        foo(1)
        foo("str")


if __name__ == "__main__":
    unittest.main()