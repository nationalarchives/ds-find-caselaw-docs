"""Tests for :class:`PreCommitYamlValidCheck`."""

from __future__ import annotations

from audit_repo_config import PreCommitYamlValidCheck
from fake_client import FakeGitHubClient, RepoStub, make_context


def test_passes_when_yaml_is_valid_mapping() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", "repos: []\n")),
    )
    ctx = make_context(client)
    assert PreCommitYamlValidCheck().run(ctx) is True


def test_fails_when_root_is_not_a_mapping() -> None:
    client = FakeGitHubClient(
        default=RepoStub(pre_commit=(".pre-commit-config.yaml", "[1, 2, 3]\n")),
    )
    ctx = make_context(client)
    assert PreCommitYamlValidCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
