#!/usr/bin/env python3
"""
test for github client class
"""
import unittest
from unittest import mock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


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

    @mock.patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test public repo"""

        mock_get_json.return_value = [{'name': 'google'}]

        with mock.patch("client.GithubOrgClient._public_repos_url",
                        new_callable=mock.PropertyMock
                        ) as mock_public_repos_url:
            payload = {'name': 'google'}
            mock_public_repos_url.return_value = payload
            mockq = GithubOrgClient("google")
            data = mockq.public_repos()
            self.assertEqual(list(payload.values()), data)
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"repo": {"license": {"key": "my_license"}},
         "license_key": "my_license"}, True),
        ({"repo": {"license": {"key": "other_license"}},
         "license_key": "my_license"}, False)
    ])
    def test_has_license(self, input: Dict[str, Dict[str, str]],
                         expected: bool):
        """Test has license method"""
        self.assertEqual(GithubOrgClient.has_license(**input), expected)
