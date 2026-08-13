"""
------------------------------------------------------------------------
Normalize a UN WPP API token into the bare value the API expects.

People paste this token from the Data Portal, from a password manager or
out of a secret box, and it arrives in several shapes: on its own, with a
"Bearer " prefix, wrapped in quotes, as a whole Authorization header, or
with trailing whitespace.  All of them mean the same token, so all of
them are accepted.

This module deliberately imports nothing outside the standard library.
It is used both by the data fetch, which runs inside the conda
environment, and by the token expiry check, which runs before that
environment exists.
------------------------------------------------------------------------
"""

# Import packages
import re

# \b so "bearer" on its own reduces to nothing and is reported as a
# missing token, while an opaque token like "bearertoken123" is untouched.
BEARER_PREFIX = re.compile(r"^bearer\b\s*", re.IGNORECASE)
HEADER_PREFIX = re.compile(r"^authorization\s*:\s*", re.IGNORECASE)
QUOTE_PAIRS = ("''", '""')


def normalize(un_token):
    """
    This function reduces a pasted UN WPP API token to its bare value.

    Args:
        un_token (str): token as pasted, may be None

    Returns:
        un_token (str): bare token, empty string when nothing was given
    """
    un_token = (un_token or "").strip()
    # Quotes first: a pasted shell value can wrap everything that follows.
    for pair in QUOTE_PAIRS:
        if len(un_token) >= 2 and un_token[0] == pair[0]:
            if un_token[-1] == pair[1]:
                un_token = un_token[1:-1].strip()
                break
    un_token = HEADER_PREFIX.sub("", un_token).strip()
    un_token = BEARER_PREFIX.sub("", un_token).strip()

    return un_token
