"""Tests for :class:`DeploymentDocumentationCheck`."""

from __future__ import annotations

from datetime import date

import pytest
from audit_repo_config import DEPLOY_MD_RELATIVE_PATH, DeploymentDocumentationCheck
from fake_client import FakeGitHubClient, RepoStub, make_context

# Fixed "today" so last_review freshness is deterministic in tests.
_REF_TODAY = date(2026, 4, 8)
_COMMENT_OK = "<!-- last_review: 2026-04-08 -->"
_COMMENT_STALE = "<!-- last_review: 2024-01-01 -->"


@pytest.fixture(autouse=True)
def _fixed_deployment_audit_today(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("audit_repo_config.deployment_audit_today", lambda: _REF_TODAY)


_README_WITH_DEPLOYMENT = f"""# Sample

## Deployment

{_COMMENT_OK}

Ship with care.
"""

_README_WITHOUT = """# Sample

## Something else

No deploy section here.
"""


def test_passes_when_readme_has_deployment_heading_and_last_review() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": _README_WITH_DEPLOYMENT},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is True


def test_passes_when_docs_deploy_md_exists_with_last_review_even_if_readme_sparse() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={
                "README.md": _README_WITHOUT,
                DEPLOY_MD_RELATIVE_PATH: f"# Deployment\n\n{_COMMENT_OK}\n",
            },
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is True


def test_passes_when_both_readme_and_deploy_doc_exist_each_has_last_review() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={
                "README.md": _README_WITH_DEPLOYMENT,
                DEPLOY_MD_RELATIVE_PATH: f"# Deployment\n\n{_COMMENT_OK}\n",
            },
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is True


def test_fails_when_neither_readme_heading_nor_deploy_file() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": _README_WITHOUT},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("FAIL" in line for line in ctx.log.lines)


def test_fails_when_readme_has_deployment_but_no_last_review_comment() -> None:
    body = """# Sample

## Deployment

Ship with care.
"""
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": body},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("first line with content after the Deployment heading" in line for line in ctx.log.lines)


def test_fails_when_last_review_date_is_too_old() -> None:
    body = f"""# Sample

## Deployment

{_COMMENT_STALE}

Ship with care.
"""
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": body},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("older than one year" in line for line in ctx.log.lines)


def test_fails_when_last_review_date_is_invalid() -> None:
    body = """# Sample

## Deployment

<!-- last_review: 2026-13-40 -->

Ship with care.
"""
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": body},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("invalid last_review" in line for line in ctx.log.lines)


def test_fails_when_last_review_exists_but_not_first_content_line_after_heading() -> None:
    body = f"""# Sample

## Deployment

Some prose before the tag.

{_COMMENT_OK}
"""
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": body},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("first line with content after the Deployment heading" in line for line in ctx.log.lines)


def test_fails_when_last_review_only_appears_later_in_readme() -> None:
    body = f"""# Sample

## Other

{_COMMENT_OK}

## Deployment

Intro paragraph.
"""
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={"README.md": body},
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any("first line with content after the Deployment heading" in line for line in ctx.log.lines)


def test_fails_when_deploy_md_present_but_missing_comment_while_readme_also_qualifies() -> None:
    """If both deployment surfaces exist, each must carry ``last_review`` on the line after ``Deployment``."""

    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={
                "README.md": _README_WITH_DEPLOYMENT,
                DEPLOY_MD_RELATIVE_PATH: "# Deployment\n\nNo HTML comment here.\n",
            },
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any(DEPLOY_MD_RELATIVE_PATH in line for line in ctx.log.lines)


def test_fails_when_deploy_md_has_no_deployment_heading() -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            pre_commit=(".pre-commit-config.yaml", "repos: []\n"),
            files={
                "README.md": _README_WITHOUT,
                DEPLOY_MD_RELATIVE_PATH: f"# How to ship\n\n{_COMMENT_OK}\n",
            },
        ),
    )
    ctx = make_context(client)
    assert DeploymentDocumentationCheck().run(ctx) is False
    assert any('no heading titled "Deployment"' in line for line in ctx.log.lines)
