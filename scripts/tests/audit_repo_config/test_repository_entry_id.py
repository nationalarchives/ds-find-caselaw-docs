"""Tests for :func:`repository_entry_id`."""

from __future__ import annotations

import pytest
from audit_repo_config import repository_entry_id


def test_raises_when_entry_is_not_a_dict() -> None:
    with pytest.raises(ValueError, match="must be a JSON object"):
        repository_entry_id("not-a-dict", 0)
