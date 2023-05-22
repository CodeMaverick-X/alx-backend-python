#!/usr/bin/env python3
"""
test utils module
"""

from utils import access_nested_map
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """test case suit"""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test the access nested map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
            ({}, ("a",)),
            ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map, path):
        """test exception"""
        with self.assertRaises(KeyError):
            try:
                access_nested_map(nested_map, path)
            except KeyError as e:
                self.assertIn(e.args[0], path)
                raise
