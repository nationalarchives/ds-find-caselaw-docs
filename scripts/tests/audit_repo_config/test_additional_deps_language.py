"""Tests for :class:`AdditionalDepsLanguageCheck`."""

from __future__ import annotations

from audit_repo_config import AdditionalDepsLanguageCheck
from fake_client import FakeGitHubClient, RepoStub, make_context

_HOOK_WITH_DEPS_NO_LANG = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        additional_dependencies: [flake8==6.0.0]
"""

_HOOK_WITH_DEPS_AND_LANG = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: python
        additional_dependencies: [flake8==6.0.0]
"""


def test_passes_when_hooks_with_additional_dependencies_have_language() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _HOOK_WITH_DEPS_AND_LANG)),
    )
    ctx = make_context(client)
    assert AdditionalDepsLanguageCheck().run(ctx) is True


def test_fails_when_additional_dependencies_present_but_language_missing() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _HOOK_WITH_DEPS_NO_LANG)),
    )
    ctx = make_context(client)
    assert AdditionalDepsLanguageCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)


_HOOK_WITH_DEPS_NONSTRING_LANG = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.0
    hooks:
      - id: trailing-whitespace
        language: 123
        additional_dependencies: [flake8==6.0.0]
"""


def test_fails_when_language_is_not_a_string() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", _HOOK_WITH_DEPS_NONSTRING_LANG)),
    )
    ctx = make_context(client)
    assert AdditionalDepsLanguageCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
    assert any("int" in line for line in ctx.log.lines)
