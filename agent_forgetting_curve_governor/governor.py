"""Ebbinghaus forgetting curve memory governor."""
import math
import time
from typing import Dict, List, Any, Optional


class MemoryItem:
    def __init__(self, key: str, value: Any, stability: float = 1.0):
        self.key = key
        self.value = value
        self.stability = max(0.1, float(stability))
        self.last_accessed = time.time()
        self.access_count = 1

    def access(self):
        # Spaced repetition reinforcement
        self.last_accessed = time.time()
        self.access_count += 1
        self.stability *= 1.8

    def retention(self, current_time: Optional[float] = None) -> float:
        now = current_time if current_time is not None else time.time()
        elapsed = max(0.0, now - self.last_accessed)
        # Ebbinghaus: R = exp(-elapsed / stability)
        return math.exp(-elapsed / (self.stability * 100.0))


class ForgettingGovernor:
    def __init__(self, prune_threshold: float = 0.25):
        self.prune_threshold = prune_threshold
        self._items: Dict[str, MemoryItem] = {}

    def record_memory(self, key: str, value: Any, stability: float = 1.0) -> MemoryItem:
        if key in self._items:
            item = self._items[key]
            item.value = value
            item.access()
            return item
        item = MemoryItem(key, value, stability)
        self._items[key] = item
        return item

    def recall_memory(self, key: str) -> Optional[Any]:
        if key in self._items:
            item = self._items[key]
            item.access()
            return item.value
        return None

    def prune(self, current_time: Optional[float] = None) -> List[str]:
        pruned = []
        for key, item in list(self._items.items()):
            if item.retention(current_time) < self.prune_threshold:
                pruned.append(key)
                del self._items[key]
        return pruned

    def get_active_memories(self) -> Dict[str, Any]:
        return {k: v.value for k, v in self._items.items()}
