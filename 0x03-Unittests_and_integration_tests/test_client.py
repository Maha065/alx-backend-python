#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://example.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")

        def side_effect(url):
            mock_response = unittest.mock.Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "http://example.com/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()


import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.public_repos methods."""

    def test_public_repos(self):
        """Test that public_repos returns all repository names."""
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url, patch("client.get_json") as mock_get_json:
            mock_repos_url.return_value = "http://example.com/repos"
            mock_get_json.return_value = repos_payload

            result = client.public_repos()
            self.assertEqual(result, expected_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")

    def test_public_repos_with_license(self):
        """Test that public_repos filters repositories by license."""
        client = GithubOrgClient("test_org")

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url, patch("client.get_json") as mock_get_json:
            mock_repos_url.return_value = "http://example.com/repos"
            mock_get_json.return_value = repos_payload

            result = client.public_repos(license="apache-2.0")
            self.assertEqual(result, apache2_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")


if __name__ == "__main__":
    unittest.main()
