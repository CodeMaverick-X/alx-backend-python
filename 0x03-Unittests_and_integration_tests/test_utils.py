#!/usr/bin/env python3
"""
test utils module
"""
from typing import Dict, Union, Tuple
from utils import access_nested_map, get_json, requests
import unittest
from parameterized import parameterized
from unittest import mock


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


class TestGetJson(unittest.TestCase):
    """test get_json"""

    @parameterized.expand([("http://example.com", {"payload": True}),
                           ("http://holberton.io", {"payload": False})])
    @mock.patch("utils.requests")
    def test_get_json(self, test_url: str, test_payload: Dict[str, bool],
                      mock_requests: mock.Mock):
        """Test Get JSON"""

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_payload
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_json(
            test_url), mock_response.json())
        mock_requests.get.assert_called_with(test_url)
