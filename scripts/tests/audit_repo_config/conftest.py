"""Pytest configuration for audit_repo_config tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def repo_id() -> str:
    return "sample-repo"
