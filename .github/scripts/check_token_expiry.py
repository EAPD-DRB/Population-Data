"""
------------------------------------------------------------------------
Fail the data-update workflow early when the UN WPP API token has
expired, and warn while there is still time to request a replacement.

The token is a JWT, so its expiry is readable from the payload without
calling the API.  Only the expiry date is ever printed -- never the
token itself.
------------------------------------------------------------------------
"""

# Import packages
import base64
import datetime
import json
import os
import sys

WARN_WITHIN_DAYS = 30
REQUEST_HELP = (
    "Generate a new token at "
    "https://population.un.org/dataportalapi/index.html (the green "
    "'Generate Token' button), then update the UN_API_TOKEN secret."
)


def token_expiry(token):
    """
    This function reads the expiry timestamp out of a JWT payload

    Args:
        token (str): UN WPP API token

    Returns:
        expires (datetime): expiry date of the token, or None if the
            token is not a JWT or carries no expiry
    """
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    parts = token.split(".")
    if len(parts) != 3:
        return None
    payload = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        claims = json.loads(base64.urlsafe_b64decode(payload))
    except (ValueError, TypeError):
        return None
    if "exp" not in claims:
        return None

    return datetime.datetime.fromtimestamp(
        claims["exp"], datetime.timezone.utc
    )


def main():
    token = os.environ.get("UN_API_TOKEN", "").strip()
    if not token:
        print("::error::UN_API_TOKEN is empty or not set. " + REQUEST_HELP)
        return 1

    expires = token_expiry(token)
    if expires is None:
        # Not fatal: a non-JWT token may still be accepted by the API.
        print("::warning::Could not read an expiry date from UN_API_TOKEN.")
        return 0

    days_left = (expires - datetime.datetime.now(datetime.timezone.utc)).days
    print(
        "UN_API_TOKEN expires {d:%Y-%m-%d} ({n} days left)".format(
            d=expires, n=days_left
        )
    )

    if days_left < 0:
        print(
            "::error::UN_API_TOKEN expired on {d:%Y-%m-%d}. {h}".format(
                d=expires, h=REQUEST_HELP
            )
        )
        return 1
    if days_left < WARN_WITHIN_DAYS:
        print(
            "::warning::UN_API_TOKEN expires in {n} days. {h}".format(
                n=days_left, h=REQUEST_HELP
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
