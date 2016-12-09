import pytest

def multiply(a,b):
    return a
class TestUM:
    def setup(self):
        print("setup             class:TestStuff")

    def teardown(self):
        print("teardown          class:TestStuff")

    def setup_class(cls):
        print("setup_class       class:%s" % cls.__name__)

    def teardown_class(cls):
        print("teardown_class    class:%s" % cls.__name__)

    def setup_method(self, method):
        print("setup_method      method:%s" % method.__name__)

    def teardown_method(self, method):
        print("teardown_method   method:%s" % method.__name__)

    def test_numbers_5_6(self):
        print
        'test_numbers_5_6  <============================ actual test code'
        assert multiply(5, 6) == 30

    def test_strings_b_2(self):
        print
        'test_strings_b_2  <============================ actual test code'
        assert multiply('b', 2) == 'bb'