"""Tests for audit aggregation and printed summaries (:func:`_run_audits`, :func:`main`)."""

from __future__ import annotations

from typing import cast

from audit_repo_config import (
    GitHubRepoAccessibleCheck,
    GitHubRepoClient,
    RepoAccess,
    RepositoryConfigAudit,
    _run_audits,
)
from audit_repo_config import (
    main as audit_main,
)
from fake_client import FakeGitHubClient, RepoStub


def test_run_audits_records_per_repo_outcomes_and_failure_counts() -> None:
    client = FakeGitHubClient(
        repos={
            "alpha": RepoStub(access=RepoAccess(True, "main")),
            "beta": RepoStub(
                access=RepoAccess(False, None, "GitHub API returned 404 for nationalarchives/beta", 404),
            ),
        },
    )
    auditor = RepositoryConfigAudit(
        cast("GitHubRepoClient", client),
        checks=[GitHubRepoAccessibleCheck()],
    )
    repos = [{"id": "alpha"}, {"id": "beta"}]

    fatal, any_failed, failure_counts, repo_outcomes = _run_audits(auditor, repos, verbose=False)

    assert fatal is None
    assert any_failed is True
    assert failure_counts["GitHub repository is reachable via the API"] == 1
    assert repo_outcomes == [
        ("alpha", True, 0),
        ("beta", False, 1),
    ]


def test_main_all_pass_prints_success_and_green_checkmark(monkeypatch, capsys) -> None:
    client = FakeGitHubClient(default=RepoStub(access=RepoAccess(True, "main")))
    monkeypatch.setattr("audit_repo_config.load_repositories", lambda: [{"id": "good-repo"}])
    monkeypatch.setattr(
        "audit_repo_config.GitHubRepoClient",
        lambda token=None: cast("GitHubRepoClient", client),
    )
    monkeypatch.setattr(
        "audit_repo_config.default_audit_checks",
        lambda: [GitHubRepoAccessibleCheck()],
    )

    code = audit_main([])

    out = capsys.readouterr().out
    assert code == 0
    assert "All repositories passed." in out
    assert "Repository summary:" in out
    assert "✅ good-repo  passed" in out
    assert "(audited 1 repositories)" in out


def test_main_failure_prints_summary_counts_and_red_x(monkeypatch, capsys) -> None:
    client = FakeGitHubClient(
        default=RepoStub(
            access=RepoAccess(False, None, "GitHub API returned 404 for nationalarchives/bad-repo", 404),
        ),
    )
    monkeypatch.setattr("audit_repo_config.load_repositories", lambda: [{"id": "bad-repo"}])
    monkeypatch.setattr(
        "audit_repo_config.GitHubRepoClient",
        lambda token=None: cast("GitHubRepoClient", client),
    )
    monkeypatch.setattr(
        "audit_repo_config.default_audit_checks",
        lambda: [GitHubRepoAccessibleCheck()],
    )

    code = audit_main([])

    out = capsys.readouterr().out
    assert code == 1
    assert "All repositories passed." not in out
    assert "Summary (repositories failing each rule):" in out
    assert "GitHub repository is reachable via the API: 1" in out
    assert "❌ bad-repo  failed (1 check)" in out
