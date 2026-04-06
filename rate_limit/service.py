from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:
    def __init__(self, limit=5, window_seconds=60, cooldown_seconds=120, strike_limit=3):
        self.limit = limit
        self.window = timedelta(seconds=window_seconds)
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.strike_limit = strike_limit
        self.requests = defaultdict(deque)
        self.strikes = defaultdict(int)
        self.banned_until = {}

    def check(self, user_id, ip_address):
        now = datetime.utcnow()
        key = f"{user_id}:{ip_address}"

        if key in self.banned_until and now < self.banned_until[key]:
            remaining = int((self.banned_until[key] - now).total_seconds())
            return {
                "allowed": False,
                "message": f"Temporary cooldown active. Try again in {remaining} seconds.",
            }

        entries = self.requests[key]
        while entries and now - entries[0] > self.window:
            entries.popleft()

        if len(entries) >= self.limit:
            self.strikes[key] += 1
            if self.strikes[key] >= self.strike_limit:
                self.banned_until[key] = now + self.cooldown
                self.strikes[key] = 0
                return {
                    "allowed": False,
                    "message": "Too many repeated requests. Temporary cooldown applied.",
                }
            return {
                "allowed": False,
                "message": "Rate limit exceeded. Please slow down and try again.",
            }

        entries.append(now)
        return {
            "allowed": True,
            "message": "Request allowed.",
        }
