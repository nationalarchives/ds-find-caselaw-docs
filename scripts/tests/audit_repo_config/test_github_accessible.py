"""Tests for :class:`GitHubRepoAccessibleCheck`."""

from __future__ import annotations

from audit_repo_config import GitHubRepoAccessibleCheck, RepoAccess
from fake_client import FakeGitHubClient, RepoStub, make_context


def test_passes_when_repository_is_reachable() -> None:
    client = FakeGitHubClient(default=RepoStub(access=RepoAccess(True, "main")))
    ctx = make_context(client)
    assert GitHubRepoAccessibleCheck().run(ctx) is True


def test_fails_when_repository_returns_404() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            access=RepoAccess(False, None, "GitHub API returned 404 for nationalarchives/sample-repo", 404),
        ),
    )
    ctx = make_context(client)
    assert GitHubRepoAccessibleCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
