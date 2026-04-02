"""Fake GitHub client and helpers for audit tests (no network)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

from audit_repo_config import AuditContext, AuditLog, GitHubRepoClient, RepoAccess


@dataclass
class RepoStub:
    """Per-repository responses for :class:`FakeGitHubClient`."""

    access: RepoAccess = field(default_factory=lambda: RepoAccess(True, "main"))
    pre_commit: tuple[str | None, str | None] = (None, None)
    files: dict[str, str | None] = field(default_factory=dict)


class FakeGitHubClient:
    """Minimal stand-in for :class:`audit_repo_config.GitHubRepoClient`."""

    def __init__(self, repos: dict[str, RepoStub] | None = None, *, default: RepoStub | None = None) -> None:
        self._repos = dict(repos or {})
        self._default = default or RepoStub()

    def _stub(self, repo_id: str) -> RepoStub:
        return self._repos.get(repo_id, self._default)

    def get_repo_access(self, repo_id: str) -> RepoAccess:
        return self._stub(repo_id).access

    def fetch_pre_commit_config(self, repo_id: str) -> tuple[str | None, str | None]:
        return self._stub(repo_id).pre_commit

    def fetch_repo_text_file(self, repo_id: str, relative_path: str) -> str | None:
        key = relative_path.lstrip("/")
        return self._stub(repo_id).files.get(key)


def make_context(
    client: FakeGitHubClient,
    *,
    repo_id: str = "sample-repo",
    verbose: bool = False,
) -> AuditContext:
    return AuditContext(
        client=cast("GitHubRepoClient", client),
        repo={"id": repo_id},
        log=AuditLog(verbose),
    )
