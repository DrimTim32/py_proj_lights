"""This file contains tests for drawing helpers"""
import sys
import unittest

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock, patch
else:
    import mock
    from mock import PropertyMock, patch

if "core" not in sys.path[0]:
    sys.path.insert(0, 'core')
from drawing.drawing_helpers import draw_car_by_value, draw_car


class MockingTestTestCase(unittest.TestCase):
    @patch('drawing.drawing_helpers.draw_car')
    def test_mock_stubs(self, draw_car):
        draw_car_by_value(None, 30, -1)
        draw_car_by_value(None, 30, 0)
        draw_car_by_value(None, 30, 1)
        draw_car_by_value(None, 30, 2)
        draw_car_by_value(None, 30, 3)
        calls = draw_car.mock_calls
        assert len(calls) == 5
        print(calls)
        draw_car.assert_any_call(None, 30, (255, 255, 255))
        draw_car.assert_any_call(None, 30, (200, 0, 0))
        draw_car.assert_any_call(None, 30, (0, 200, 0))
        draw_car.assert_any_call(None, 30, (0, 0, 200))
        draw_car.assert_any_call(None, 30, (255, 0, 114))
