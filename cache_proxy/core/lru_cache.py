"""
LRU cache implemented from scratch with a hashmap and a doubly linked list.

The hashmap gives O(1) lookup by key. The linked list gives O(1) promotion
to "most recently used" and O(1) eviction of the "least recently used" item.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.prev: _Node[K, V] | None = None
        self.next: _Node[K, V] | None = None


class LRUCache(Generic[K, V]):
    """Fixed-size LRU cache.

    New and recently accessed nodes live near the head.
    Old nodes drift toward the tail and are evicted first.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be greater than 0")

        self.capacity = capacity
        self._items: dict[K, _Node[K, V]] = {}

        self._head: _Node[K, V] | None = None
        self._tail: _Node[K, V] | None = None

    def get(self, key: K) -> V | None:
        """Return a cached value and mark it as recently used."""
        node = self._items.get(key)
        if node is None:
            return None

        self._move_to_head(node)
        return node.value

    def peek(self, key: K) -> V | None:
        """Return a cached value without changing recency order."""
        node = self._items.get(key)
        if node is None:
            return None
        return node.value

    def set(self, key: K, value: V) -> None:
        """Insert or update a value, evicting the LRU item when full."""
        node = self._items.get(key)

        if node is not None:
            node.value = value
            self._move_to_head(node)
            return

        node = _Node(key, value)
        self._items[key] = node
        self._add_to_head(node)

        if len(self._items) > self.capacity:
            self._evict_tail()

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def delete(self, key: K) -> bool:
        """Delete a key if present. Returns True when something was removed."""
        node = self._items.pop(key, None)
        if node is None:
            return False

        self._unlink(node)
        return True

    def clear(self) -> None:
        self._items.clear()
        self._head = None
        self._tail = None

    def keys(self) -> Iterator[K]:
        """Yield keys from most recently used to least recently used."""
        current = self._head
        while current is not None:
            yield current.key
            current = current.next

    def items(self) -> Iterator[tuple[K, V]]:
        """Yield items from most recently used to least recently used."""
        current = self._head
        while current is not None:
            yield current.key, current.value
            current = current.next

    def _move_to_head(self, node: _Node[K, V]) -> None:
        if node is self._head:
            return
        self._unlink(node)
        self._add_to_head(node)

    def _add_to_head(self, node: _Node[K, V]) -> None:
        node.prev = None
        node.next = self._head

        if self._head is not None:
            self._head.prev = node

        self._head = node

        if self._tail is None:
            self._tail = node

    def _unlink(self, node: _Node[K, V]) -> None:
        previous_node = node.prev
        next_node = node.next

        if previous_node is None:
            self._head = next_node
        else:
            previous_node.next = next_node

        if next_node is None:
            self._tail = previous_node
        else:
            next_node.prev = previous_node

        node.prev = None
        node.next = None

    def _evict_tail(self) -> None:
        if self._tail is None:
            return

        old_tail = self._tail
        self._items.pop(old_tail.key)
        self._unlink(old_tail)

    def __contains__(self, key: object) -> bool:
        return key in self._items

    def __len__(self) -> int:
        return len(self._items)
