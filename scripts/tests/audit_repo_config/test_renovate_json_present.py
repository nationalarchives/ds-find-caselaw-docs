"""Tests for :class:`RenovateJsonPresentCheck`."""

from __future__ import annotations

from audit_repo_config import RENOVATE_JSON_FILE, RenovateJsonPresentCheck
from fake_client import FakeGitHubClient, RepoStub, make_context


def test_passes_when_renovate_json_exists() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RENOVATE_JSON_FILE: "{}\n"},
        ),
    )
    ctx = make_context(client)
    assert RenovateJsonPresentCheck().run(ctx) is True


def test_fails_when_renovate_json_missing() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={},
        ),
    )
    ctx = make_context(client)
    assert RenovateJsonPresentCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)
