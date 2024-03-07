import requests
import time
import functools

"""
Replace all of this! It is only meant as a reference, and intended to be
used as an importable library somewhere at or under the top level src/
directory.
"""


def rate_limit(func):
    """
    Decorator for all requests to prevent rate limiting.

    Waits at least 400ms between requests.

    https://developers.notion.com/reference/request-limits#rate-limits

    """
    REQUEST_INTERVAL_SECS = 0.4
    time_of_last_response = time.time()

    @functools.wraps(func)
    def rate_limited(*args, **kwargs):
        nonlocal time_of_last_response
        now = time.time()
        if now - time_of_last_response < REQUEST_INTERVAL_SECS:
            time.sleep(REQUEST_INTERVAL_SECS - (now - time_of_last_response))
        result = func(*args, **kwargs)
        time_of_last_response = time.time()
        # make sure we've success status code
        result.raise_for_status()
        return result

    return rate_limited


@rate_limit
def get(url, headers):
    return requests.get(url, headers=headers)


@rate_limit
def post(url, headers, json):
    return requests.post(url, headers=headers, json=json)


@rate_limit
def patch(url, headers, json):
    return requests.patch(url, headers=headers, json=json)
