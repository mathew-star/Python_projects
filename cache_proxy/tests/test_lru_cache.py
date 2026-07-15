import unittest

from cache_proxy.core.lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_get_promotes_item_to_most_recent(self) -> None:
        cache = LRUCache[str, int](capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)

        self.assertEqual(cache.get("a"), 1)
        cache.set("c", 3)

        self.assertIsNone(cache.get("b"))
        self.assertEqual(list(cache.keys()), ["c", "a"])

    def test_setting_existing_key_updates_value_and_recency(self) -> None:
        cache = LRUCache[str, int](capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("a", 10)

        cache.set("c", 3)

        self.assertEqual(cache.get("a"), 10)
        self.assertIsNone(cache.get("b"))

    def test_delete_removes_node_from_linked_list_and_hashmap(self) -> None:
        cache = LRUCache[str, int](capacity=3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)

        self.assertTrue(cache.delete("b"))

        self.assertNotIn("b", cache)
        self.assertEqual(list(cache.keys()), ["c", "a"])

    def test_invalid_capacity_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            LRUCache[str, int](capacity=0)


if __name__ == "__main__":
    unittest.main()
