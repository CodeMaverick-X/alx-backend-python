#!/usr/bin/env python3
"""
test for github client class
"""
import unittest
from unittest import mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """test suits fro github client class"""

    @parameterized.expand([
            ('google'),
            ('abc')
        ])
    @mock.patch('client.get_json')
    def test_org(self, name, mock_obj):
        """test org method"""

        mock_obj.return_value = {'name': 'reinhard_corp', 'age': 9}

        client = GithubOrgClient(name)
        org = client.org
        org = client.org

        mock_obj.assert_called_once()

    def test_public_repos_url(self):
        """test public repos url"""

        def getitem_mock(self, key):
            if key == 'repos_url':
                return 'fake/url'
            return base_mock.__getitem__(key)

        with mock.patch('client.GithubOrgClient.org') as mock_method:
            mock_method.return_value = {'name': 'reinhard'}
            mock_method.__getitem__ = getitem_mock

            client = GithubOrgClient('google')
            val = client._public_repos_url
            self.assertEqual(val, 'fake/url')
