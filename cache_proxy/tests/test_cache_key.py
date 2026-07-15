import unittest

from cache_proxy.core.cache_key import build_cache_key


class CacheKeyTests(unittest.TestCase):
    def test_same_request_builds_same_key(self) -> None:
        first = build_cache_key(method="get", url="https://example.com/users?id=1")
        second = build_cache_key(method="GET", url="https://example.com/users?id=1")

        self.assertEqual(first, second)

    def test_body_changes_key(self) -> None:
        first = build_cache_key(
            method="POST",
            url="https://example.com/echo",
            body=b'{"name":"mathew"}',
        )
        second = build_cache_key(
            method="POST",
            url="https://example.com/echo",
            body=b'{"name":"codex"}',
        )

        self.assertNotEqual(first, second)

    def test_vary_headers_change_key(self) -> None:
        first = build_cache_key(
            method="GET",
            url="https://example.com/report",
            headers={"Accept": "application/json"},
            vary_headers=("Accept",),
        )
        second = build_cache_key(
            method="GET",
            url="https://example.com/report",
            headers={"Accept": "text/csv"},
            vary_headers=("Accept",),
        )

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
