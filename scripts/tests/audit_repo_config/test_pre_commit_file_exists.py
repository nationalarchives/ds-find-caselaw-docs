"""Tests for :class:`PreCommitFileExistsCheck`."""

from __future__ import annotations

from audit_repo_config import PreCommitFileExistsCheck
from fake_client import FakeGitHubClient, RepoStub, make_context


def test_passes_when_pre_commit_file_exists() -> None:
    yaml_text = "repos: []\n"
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", yaml_text)),
    )
    ctx = make_context(client)
    assert PreCommitFileExistsCheck().run(ctx) is True


def test_fails_when_no_pre_commit_file() -> None:
    client = FakeGitHubClient(default=RepoStub(pre_commit=(None, None)))
    ctx = make_context(client)
    assert PreCommitFileExistsCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
