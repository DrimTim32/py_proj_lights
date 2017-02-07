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
        draw_car_by_value(None, 1, -1)
        draw_car_by_value(None, 2, 0)
        draw_car_by_value(None, 3, 1)
        draw_car_by_value(None, 4, 2)
        draw_car_by_value(None, 5, 3)
        draw_car_by_value(None, 6, 4)
        calls = draw_car.mock_calls
        assert len(calls) == 6
        draw_car.assert_any_call(None, 1, (255, 255, 255))
        draw_car.assert_any_call(None, 2, (200, 0, 0))
        draw_car.assert_any_call(None, 3, (0, 200, 0))
        draw_car.assert_any_call(None, 4, (0, 0, 200))
        draw_car.assert_any_call(None, 5, (255, 0, 114))
        draw_car.assert_any_call(None, 6, (0, 0, 0))
