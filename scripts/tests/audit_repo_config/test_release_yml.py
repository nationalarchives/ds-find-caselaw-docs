"""Tests for :class:`ReleaseYmlCheck` and :class:`ReleaseYmlConfigRules`."""

from __future__ import annotations

from typing import cast

from audit_repo_config import (
    RELEASE_YML_RELATIVE_PATH,
    AuditContext,
    AuditLog,
    GitHubRepoClient,
    ReleaseYmlCheck,
    ReleaseYmlConfigRules,
)
from fake_client import FakeGitHubClient, RepoStub, make_context

_MIN_VALID_RELEASE_YML = """changelog:
  categories:
    - title: Other Changes
      labels:
        - "*"
"""


def test_skips_when_hide_releases_true() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={},
        ),
    )
    ctx = AuditContext(
        client=cast("GitHubRepoClient", client),
        repo={"id": "sample-repo", "hide_releases": True},
        log=AuditLog(verbose=True),
    )
    assert ReleaseYmlCheck().run(ctx) is True
    assert any("SKIP" in line and "hide_releases" in line for line in ctx.log.lines)


def test_passes_when_release_yml_valid() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RELEASE_YML_RELATIVE_PATH: _MIN_VALID_RELEASE_YML},
        ),
    )
    ctx = make_context(client)
    assert ReleaseYmlCheck().run(ctx) is True


def test_fails_when_release_yml_missing() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={},
        ),
    )
    ctx = make_context(client)
    assert ReleaseYmlCheck().run(ctx) is False


def test_fails_when_release_yml_invalid_yaml() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RELEASE_YML_RELATIVE_PATH: "changelog: [\n"},
        ),
    )
    ctx = make_context(client)
    assert ReleaseYmlCheck().run(ctx) is False


def test_validation_errors_empty_categories() -> None:
    text = "changelog:\n  categories: []\n"
    err = ReleaseYmlConfigRules.validation_errors(text)
    assert any("empty" in e for e in err)


def test_validation_errors_category_without_title() -> None:
    text = """changelog:
  categories:
    - labels:
        - "*"
"""
    err = ReleaseYmlConfigRules.validation_errors(text)
    assert any("title" in e for e in err)
