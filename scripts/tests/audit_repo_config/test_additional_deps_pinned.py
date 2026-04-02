"""Tests for :class:`AdditionalDepsPinnedCheck`."""

from __future__ import annotations

from audit_repo_config import AdditionalDepsPinnedCheck
from fake_client import FakeGitHubClient, RepoStub, make_context

_PINNED = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: python
        additional_dependencies: [flake8==6.0.0]
"""

_UNPINNED = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: python
        additional_dependencies: [flake8]
"""

_NPM_PINNED = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: node
        additional_dependencies: ["@acme/widget@2.0.0"]
"""

_NPM_RANGE = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: node
        additional_dependencies: ["@acme/widget@^2.0.0"]
"""


def test_passes_when_additional_dependencies_are_pinned() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _PINNED)),
    )
    ctx = make_context(client)
    assert AdditionalDepsPinnedCheck().run(ctx) is True


def test_fails_when_additional_dependency_is_not_pinned() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _UNPINNED)),
    )
    ctx = make_context(client)
    assert AdditionalDepsPinnedCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)


def test_passes_when_npm_scoped_dependency_has_exact_version() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _NPM_PINNED)),
    )
    ctx = make_context(client)
    assert AdditionalDepsPinnedCheck().run(ctx) is True


def test_fails_when_npm_scoped_dependency_uses_semver_range() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _NPM_RANGE)),
    )
    ctx = make_context(client)
    assert AdditionalDepsPinnedCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
