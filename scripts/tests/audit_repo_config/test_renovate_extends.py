"""Tests for :class:`RenovateExtendsCheck`."""

from __future__ import annotations

import json

from audit_repo_config import RENOVATE_EXTENDS_REQUIRED, RENOVATE_JSON_FILE, RenovateExtendsCheck
from fake_client import FakeGitHubClient, RepoStub, make_context

_EXTENDS_OK = json.dumps({"extends": [RENOVATE_EXTENDS_REQUIRED]})
_EXTENDS_WRONG = json.dumps({"extends": ["some-other/config"]})


def test_passes_when_extends_includes_required_preset() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RENOVATE_JSON_FILE: _EXTENDS_OK},
        ),
    )
    ctx = make_context(client)
    assert RenovateExtendsCheck().run(ctx) is True


def test_fails_when_extends_omits_required_preset() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RENOVATE_JSON_FILE: _EXTENDS_WRONG},
        ),
    )
    ctx = make_context(client)
    assert RenovateExtendsCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)


def test_fails_when_renovate_json_is_missing() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={},
        ),
    )
    ctx = make_context(client)
    assert RenovateExtendsCheck().run(ctx) is False
    assert any("renovate.json not on the default branch" in line for line in ctx.log.lines)


def test_fails_when_renovate_json_is_invalid() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={RENOVATE_JSON_FILE: "{ not json"},
        ),
    )
    ctx = make_context(client)
    assert RenovateExtendsCheck().run(ctx) is False
    assert any("invalid JSON" in line for line in ctx.log.lines)
