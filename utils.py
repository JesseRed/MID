#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions and classes for MID task.
"""

import random
from datetime import datetime


def timestamp():
    """Generate timestamp string."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def uniform_jitter(lo, hi):
    """Generate uniform random jitter between lo and hi."""
    return random.uniform(lo, hi)


class StaircaseAdaptive:
    """Simple 1-up/2-down staircase to converge at ~70%."""
    
    def __init__(self, initial_ms, min_ms, max_ms, step_ms):
        self.value = initial_ms
        self.min_ms = min_ms
        self.max_ms = max_ms
        self.step = step_ms
        self._consecutive_hits = 0

    def update(self, hit):
        """Update staircase based on hit/miss."""
        if hit:
            self._consecutive_hits += 1
            if self._consecutive_hits >= 2:
                self.value = max(self.min_ms, self.value - self.step)
                self._consecutive_hits = 0
        else:
            self.value = min(self.max_ms, self.value + self.step)
            self._consecutive_hits = 0

    def get_ms(self):
        """Get current target duration in milliseconds."""
        return self.value
