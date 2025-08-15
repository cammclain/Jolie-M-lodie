'''
This file contains the models for the invite code, and the response handling.

'''
# Module-level docstring:
# - States purpose: data models for invite codes and responses.
# - Good for quick context and doc tooling. Could expand with data constraints or usage.

import datetime as dt
# Imports the standard library datetime module under the alias `dt`.
# - Using an alias keeps type annotations shorter (dt.datetime vs datetime.datetime).
# - Consider timezone awareness (naive vs aware datetimes) for correctness.

import reflex as rx
# Imports Reflex (formerly Pynecone) as `rx`.
# - rx.Model below indicates these classes are database-backed models integrated with Reflex’s ORM layer.

from typing import Optional
# Imports Optional for nullable type hints (value or None).
# - In Python 3.10+, you can also write `datetime | None` as a shorthand.

class InviteCode(rx.Model, table=True):
    # Declares a Reflex model named InviteCode.
    # - `rx.Model` integrates Pydantic/SQLModel-like behavior (validation + persistence).
    # - `table=True` instructs Reflex to create a corresponding DB table for this model.

    code: str                    # store a short random string
    # The invite code itself.
    # - Likely should be unique and indexed for lookups.
    # - Consider length constraints and allowed character set.

    expires_at: Optional[dt.datetime] = None
    # When the code becomes invalid.
    # - Optional means codes can be non-expiring (None).
    # - Decide on timezone policy; store UTC and enforce awareness if possible.

    used_at: Optional[dt.datetime] = None
    # When the code was redeemed.
    # - None means unused.
    # - Setting this may be part of an atomic redemption flow to prevent reuse.

class Response(rx.Model, table=True):
    # Declares a Reflex model named Response.
    # - Name may collide conceptually with common web "Response" types; consider a more specific name (e.g., InviteResponse/Submission).

    code: str                    # copy the code here for easy lookups
    # Denormalized copy of the invite code string.
    # - Speeds up querying responses by code without a join.
    # - Consider a foreign key to InviteCode for referential integrity in addition to (or instead of) duplication.

    q_name: str
    # The respondent’s name as free text.
    # - Consider max length and validation (non-empty).

    q_email: str
    # The respondent’s email as free text.
    # - Prefer an email type/validator (e.g., Pydantic EmailStr) to ensure valid format.

    q_feedback: str
    # Free-form feedback text.
    # - Might be long; ensure DB column can accommodate (TEXT vs short VARCHAR).