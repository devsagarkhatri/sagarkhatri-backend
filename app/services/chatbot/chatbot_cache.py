
from collections import OrderedDict
from threading import Lock
from time import monotonic


CACHE_TTL_SECONDS = 300
MAX_CACHE_ENTRIES = 500

_cache: OrderedDict[str, tuple[str, float]] = OrderedDict()
_lock = Lock()


def _normalize_question(question: str) -> str:
    return " ".join(question.split()).casefold()


def get_cached_answer(question: str) -> str | None:
    key = _normalize_question(question)

    if not key:
        return None

    now = monotonic()

    with _lock:
        entry = _cache.get(key)

        if entry is None:
            return None

        answer, expires_at = entry

        if now >= expires_at:
            del _cache[key]
            return None

        # Move recently used entries to the end.
        _cache.move_to_end(key)
        return answer


def cache_answer(question: str, answer: str) -> None:
    key = _normalize_question(question)

    if not key or not isinstance(answer, str) or not answer.strip():
        return

    with _lock:
        _cache[key] = (
            answer,
            monotonic() + CACHE_TTL_SECONDS,
        )
        _cache.move_to_end(key)

        while len(_cache) > MAX_CACHE_ENTRIES:
            _cache.popitem(last=False)


def clear_chatbot_cache() -> None:
    """Clear cached answers after portfolio content changes."""
    with _lock:
        _cache.clear()
