"""Non-blocking, local-only background generation of static UI language packs.

The worker translates catalog strings exclusively; it never receives user text,
medical records, credentials, or session state. One worker avoids exhausting
8 GB laptops with competing model requests. Results persist atomically through
scripts.translate_ui and remain usable on future offline runs.
"""
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from ui.strings import EXTRA_TEXT, locale_coverage
from scripts.translate_ui import prepare_language_pack

_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="hia-ui-localization")
_LOCK = Lock()
_JOBS = {}


def ensure_job(code: str):
    """Submit once; reattempt a failed/incomplete pack only on explicit retry."""
    if code not in EXTRA_TEXT:
        return "ready"
    done, total = locale_coverage(code)
    if done == total:
        return "ready"
    with _LOCK:
        job = _JOBS.get(code)
        if job is None:
            _JOBS[code] = _EXECUTOR.submit(
                prepare_language_pack, code, batch_size=6, rounds=3
            )
            return "working"
        return _job_status(job)


def _job_status(job):
    if not job.done():
        return "working"
    try:
        done, total = job.result()
    except Exception:
        return "failed"
    return "ready" if done == total else "incomplete"


def job_status(code: str):
    """Read only task status; do not unexpectedly start another generation job."""
    with _LOCK:
        job = _JOBS.get(code)
        return _job_status(job) if job else "not_started"


def retry_job(code: str):
    if code not in EXTRA_TEXT:
        return "ready"
    with _LOCK:
        job = _JOBS.get(code)
        if job is not None and not job.done():
            return "working"
        _JOBS[code] = _EXECUTOR.submit(
            prepare_language_pack, code, batch_size=6, rounds=3
        )
        return "working"
