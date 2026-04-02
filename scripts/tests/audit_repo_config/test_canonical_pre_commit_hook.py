"""Tests for :class:`CanonicalPreCommitHookCheck` (zizmor and renovate-config-validator)."""

from __future__ import annotations

from audit_repo_config import (
    RENOVATE_VALIDATOR_POLICY,
    ZIZMOR_POLICY,
    CanonicalPreCommitHookCheck,
)
from fake_client import FakeGitHubClient, RepoStub, make_context

_ZIZMOR_OK = """
repos:
  - repo: https://github.com/woodruffw/zizmor-pre-commit
    rev: v1.0.0
    hooks:
      - id: zizmor
"""

_ZIZMOR_WRONG_REPO = """
repos:
  - repo: https://github.com/example/fork-zizmor
    hooks:
      - id: zizmor
"""

_RENOVATE_VALIDATOR_OK = """
repos:
  - repo: https://github.com/renovatebot/pre-commit-hooks
    rev: v0.1.0
    hooks:
      - id: renovate-config-validator
"""

_RENOVATE_VALIDATOR_MISSING = """
repos: []
"""


def test_zizmor_passes_when_hook_uses_canonical_repository() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _ZIZMOR_OK)),
    )
    ctx = make_context(client)
    check = CanonicalPreCommitHookCheck(
        ZIZMOR_POLICY,
        "Pre-commit registers zizmor from woodruffw/zizmor-pre-commit",
    )
    assert check.run(ctx) is True


def test_zizmor_fails_when_hook_points_at_wrong_repository() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _ZIZMOR_WRONG_REPO)),
    )
    ctx = make_context(client)
    check = CanonicalPreCommitHookCheck(
        ZIZMOR_POLICY,
        "Pre-commit registers zizmor from woodruffw/zizmor-pre-commit",
    )
    assert check.run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)


def test_renovate_validator_passes_when_hook_uses_canonical_repository() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _RENOVATE_VALIDATOR_OK)),
    )
    ctx = make_context(client)
    check = CanonicalPreCommitHookCheck(
        RENOVATE_VALIDATOR_POLICY,
        "Pre-commit registers renovate-config-validator from renovatebot/pre-commit-hooks",
    )
    assert check.run(ctx) is True


def test_renovate_validator_fails_when_hook_is_absent() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _RENOVATE_VALIDATOR_MISSING)),
    )
    ctx = make_context(client)
    check = CanonicalPreCommitHookCheck(
        RENOVATE_VALIDATOR_POLICY,
        "Pre-commit registers renovate-config-validator from renovatebot/pre-commit-hooks",
    )
    assert check.run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
