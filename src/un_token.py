"""
------------------------------------------------------------------------
Normalize a UN WPP API token into the bare value the API expects.

People copy this token one of two ways: the whole line, which carries a
"Bearer " prefix, or just the token part.  Both mean the same token, so
both are accepted.  Surrounding whitespace is trimmed as well, since a
token read from a file arrives with a trailing newline.

This module deliberately imports nothing outside the standard library.
It is used both by the data fetch, which runs inside the conda
environment, and by the token expiry check, which runs before that
environment exists.
------------------------------------------------------------------------
"""

# Import packages
import re

BEARER_PREFIX = re.compile(r"^bearer\s+", re.IGNORECASE)


def normalize(un_token):
    """
    This function reduces a copied UN WPP API token to its bare value.

    Args:
        un_token (str): token as copied, may be None

    Returns:
        un_token (str): bare token, empty string when nothing was given
    """
    return BEARER_PREFIX.sub("", (un_token or "").strip())
