"""Token Bucket and Leaky Bucket Rate Limiting Engine.
100% Python Standard Library.
"""

import time

class TokenBucketLimiter:
    """Token Bucket rate limiter allowing bursts up to capacity."""
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def consume(self, amount: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False

class LeakyBucketLimiter:
    """Leaky Bucket rate limiter smoothing bursty traffic to a constant rate."""
    def __init__(self, capacity: float, leak_rate: float):
        self.capacity = float(capacity)
        self.leak_rate = float(leak_rate)
        self.water = 0.0
        self.last_leak = time.time()

    def add(self, amount: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_leak
        self.water = max(0.0, self.water - elapsed * self.leak_rate)
        self.last_leak = now
        if self.water + amount <= self.capacity:
            self.water += amount
            return True
        return False
