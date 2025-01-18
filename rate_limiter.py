from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, max_requests: int = 30, time_window: int = 60):
        self.max_requests = max_requests  # Maximum requests per time window
        self.time_window = time_window    # Time window in seconds
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, user_id: str) -> Tuple[bool, int]:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        
        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id] 
            if req_time > cutoff
        ]
        
        # Check if user has exceeded rate limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False, self._get_wait_time(user_id)
            
        # Add new request
        self.requests[user_id].append(now)
        return True, 0

    def _get_wait_time(self, user_id: str) -> int:
        if not self.requests[user_id]:
            return 0
        oldest_request = self.requests[user_id][0]
        wait_time = self.time_window - (datetime.now() - oldest_request).seconds
        return max(0, wait_time) 