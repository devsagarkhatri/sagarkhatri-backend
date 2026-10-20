
from collections import deque
from math import ceil
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request


MAX_REQUESTS_PER_MINUTE = 10
MAX_REQUESTS_PER_HOUR = 50

MINUTE_WINDOW = 60
HOUR_WINDOW = 60 * 60

_requests_by_ip: dict[str, deque[float]] = {}
_lock = Lock()
_last_cleanup = 0.0


def enforce_chat_rate_limit(request: Request) -> None:
    global _last_cleanup

    client_ip = (
        request.client.host
        if request.client is not None
        else "unknown"
    )
    now = monotonic()

    with _lock:
        # Periodically remove inactive IP addresses to bound memory use.
        if now - _last_cleanup >= 60:
            for ip in list(_requests_by_ip):
                timestamps = _requests_by_ip[ip]

                while timestamps and now - timestamps[0] >= HOUR_WINDOW:
                    timestamps.popleft()

                if not timestamps:
                    del _requests_by_ip[ip]

            _last_cleanup = now

        timestamps = _requests_by_ip.setdefault(
            client_ip,
            deque(),
        )

        while timestamps and now - timestamps[0] >= HOUR_WINDOW:
            timestamps.popleft()

        minute_requests = sum(
            1
            for timestamp in timestamps
            if now - timestamp < MINUTE_WINDOW
        )

        if minute_requests >= MAX_REQUESTS_PER_MINUTE:
            retry_after = ceil(
                timestamps[-MAX_REQUESTS_PER_MINUTE]
                + MINUTE_WINDOW
                - now
            )

            raise HTTPException(
                status_code=429,
                detail="Too many chat requests. Please try again shortly.",
                headers={"Retry-After": str(max(1, retry_after))},
            )

        if len(timestamps) >= MAX_REQUESTS_PER_HOUR:
            retry_after = ceil(
                timestamps[0] + HOUR_WINDOW - now
            )

            raise HTTPException(
                status_code=429,
                detail="Chat request limit reached. Please try again later.",
                headers={"Retry-After": str(max(1, retry_after))},
            )

        timestamps.append(now)
