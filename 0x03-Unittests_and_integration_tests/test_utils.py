import unittest
from parameterized import parameterized
from utils import access_nested_map  # assuming this is where the function lives


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({}, ("a",)),                     # empty map, missing key "a"
        ({"a": 1}, ("a", "b")),           # valid first key, missing nested key "b"
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
