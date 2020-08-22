from unittest import TestCase
from create_vot_json import format_relative_coordinates


class Test(TestCase):
    def test_format_relative_coordinates(self):
        input_coords = [
            30, 30,
            10, 10
        ]
        expected_coords = [
            30, 30,
            40, 30,
            40, 40,
            30, 40
        ]

        self.assertEquals(
            expected_coords,
            format_relative_coordinates(input_coords))

    def test_invalid_input(self):
        with self.assertRaises(expected_exception=ValueError):
            format_relative_coordinates([1, 2, 3])
