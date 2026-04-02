#!/usr/bin/env python3
"""Audit Find Case Law repos (from scripts/repositories.json) for shared config.

The implementation is class-based:

* :class:`GitHubRepoClient` — HTTP + caching for API and raw file fetches.
* :class:`AuditLog` — records ``{label}: PASS`` or ``{label}: SKIP`` when verbose, always
  records ``{label}: FAIL`` on failure, with optional indented *partial* lines for detail.
* :class:`AuditContext` — one repo per audit pass; lazy-loaded pre-commit parse and
  ``renovate.json`` text so checks share work.
* :class:`PreCommitConfigDocument` — parsed ``.pre-commit-config`` mapping plus
  dependency / hook analysis.
* :class:`CanonicalPreCommitHookPolicy` — reusable rule “hook id X must come from
  GitHub owner/repo Y” (zizmor, renovate validator).
* :class:`DeploymentDocumentationRules` / :class:`DeploymentDocumentationCheck` — README
  “Deployment” heading or ``docs/DEPLOY.md``, each present source must include a recent
  ``<!-- last_review: YYYY-MM-DD -->`` on the first non-blank line after the ``Deployment`` heading
  (not missing; date within the last year, UTC).
* :class:`AuditCheck` subclasses — one concern each; :func:`default_audit_checks`
  lists the standard suite (starting with GitHub API repository accessibility).
  :class:`RenovateJsonPresentCheck` runs before :class:`RenovateExtendsCheck`; the extends
  check still **fails** if ``renovate.json`` is absent so it cannot look like a pass.
* :class:`ReleaseYmlCheck` — for repositories without ``hide_releases`` in ``repositories.json``,
  require ``.github/release.yml`` on the default branch: valid YAML mapping root and a
  ``changelog.categories`` list of objects with non-empty ``title`` and ``labels`` (GitHub
  auto-generated release notes config).

Exit codes: ``0`` all repos pass, ``1`` at least one check failed, ``2`` invalid
``repositories.json`` entry or unexpected error while auditing a repo.

With ``-v`` / ``--verbose``, each repository lists one line per audit check: ``PASS``,
``FAIL`` (with optional partial detail), or ``SKIP`` when that check did not apply.
Without ``-v``, only repositories with at least one failure are printed, and the log
for those repos contains ``FAIL`` lines only (``PASS`` and ``SKIP`` are not recorded).

Requires PyYAML and ``requests`` (``pip install pyyaml requests``) and network access to GitHub.
The GitHub client uses ``requests`` and explicit API/raw URLs rather than PyGithub so the audit
script stays dependency-light and easy to substitute in tests (see ``scripts/tests/audit_repo_config``).

Unauthenticated GitHub API requests are rate-limited heavily (HTTP 429). Set
``GITHUB_TOKEN`` or ``GH_TOKEN``, or pass ``--token``, to use a personal access
token (``repo`` scope is enough for public repositories).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

try:
    import requests  # type: ignore[import-untyped, unused-ignore]
except ImportError:
    print("This script requires requests. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

OWNER = "nationalarchives"
PRE_COMMIT_FILENAMES = (".pre-commit-config.yaml", ".pre-commit-config.yml")
GITHUB_API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
BASE_HTTP_HEADERS: dict[str, str] = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ds-find-caselaw-docs-repo-config-audit",
}

RENOVATE_JSON_FILE = "renovate.json"
RENOVATE_EXTENDS_REQUIRED = "github>nationalarchives/ds-find-caselaw-docs"
RELEASE_YML_RELATIVE_PATH = ".github/release.yml"
DEPLOY_MD_RELATIVE_PATH = "docs/DEPLOY.md"
README_FILENAMES_FOR_DEPLOYMENT_AUDIT = ("README.md", "readme.md")

_ALLOWED_GITHUB_NETLOCS = frozenset({"api.github.com", "raw.githubusercontent.com"})
_GITHUB_REPO_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,200}$")


# ---------------------------------------------------------------------------
# Repository list
# ---------------------------------------------------------------------------


def load_repositories() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent / "repositories.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        msg = f"Expected a JSON array in {path}"
        raise TypeError(msg)
    return data


def repository_entry_id(repo: dict[str, Any], index: int) -> str:
    """Return a validated ``id`` for logging and auditing, or raise :class:`ValueError`."""
    if not isinstance(repo, dict):
        msg = f"entry #{index} must be a JSON object, not {type(repo).__name__}"
        raise ValueError(msg)  # noqa: TRY004  # treated like other invalid repositories.json rows (exit 2)
    rid = repo.get("id")
    if not isinstance(rid, str) or not rid.strip():
        msg = f"entry #{index} must have a non-empty string 'id'"
        raise ValueError(msg)
    rid = rid.strip()
    err = github_repo_id_error(rid)
    if err:
        msg = f"entry #{index} ({rid!r}): {err}"
        raise ValueError(msg)
    return rid


def github_repo_id_error(repo_id: str) -> str | None:
    """Return an error message if ``repo_id`` is not safe for GitHub URL path segments."""
    if not _GITHUB_REPO_ID_RE.fullmatch(repo_id):
        return "repository id must match GitHub naming rules (letters, digits, . _ - only)"
    return None


def _assert_https_github_url(url: str) -> None:
    """Reject non-HTTPS and unexpected hosts before issuing an HTTP request."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        msg = f"disallowed URL scheme for {url!r} (only https is permitted)"
        raise ValueError(msg)
    if parsed.netloc not in _ALLOWED_GITHUB_NETLOCS:
        msg = f"unexpected URL host for GitHub client: {parsed.netloc!r}"
        raise ValueError(msg)
    if parsed.username is not None or parsed.password is not None:
        msg = "URL must not embed user credentials"
        raise ValueError(msg)


def _validate_branch_name(branch: str) -> str | None:
    if not branch or len(branch) > 255:
        return "invalid default branch name from GitHub API"
    if any(c in branch for c in "\x00\n\r"):
        return "default branch name contains disallowed characters"
    return None


def _validate_repo_relative_path(relative_path: str) -> str | None:
    name = relative_path.lstrip("/")
    if not name or len(name) > 500:
        return "invalid relative file path"
    if ".." in name or name.startswith("/"):
        return "relative file path must not contain '..' or absolute segments"
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", name):
        return "relative file path contains disallowed characters"
    return None


# ---------------------------------------------------------------------------
# GitHub API: repository reachable?
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RepoAccess:
    """Result of ``GET /repos/{org}/{repo}`` (cached on :class:`GitHubRepoClient`).

    When ``ok`` is true, ``default_branch`` is the repo default (never None).
    When ``ok`` is false, ``block_reason`` explains why (and ``default_branch`` is None).
    """

    ok: bool
    default_branch: str | None
    block_reason: str | None = None
    http_status: int | None = None


# ---------------------------------------------------------------------------
# GitHub HTTP client (token + per-instance caches)
# ---------------------------------------------------------------------------


class GitHubRepoClient:
    """Fetches repo metadata and files from ``github.com`` / ``raw.githubusercontent.com``."""

    def __init__(self, org: str = OWNER, token: str | None = None) -> None:
        self.org = org
        self.set_token(token)

    def set_token(self, token: str | None) -> None:
        t = token.strip() if isinstance(token, str) else ""
        self._token: str | None = t or None
        self._headers: dict[str, str] = dict(BASE_HTTP_HEADERS)
        if self._token:
            self._headers["Authorization"] = f"Bearer {self._token}"
        self._clear_caches()
        self._session = requests.Session()
        self._session.headers.update(self._headers)

    def _validated_default_branch(self, repo_id: str) -> str | None:
        """Return the default branch name when the repo is reachable and the branch is safe; else ``None``."""
        access = self.get_repo_access(repo_id)
        if not access.ok or access.default_branch is None:
            return None
        branch = access.default_branch
        if _validate_branch_name(branch):
            return None
        return branch

    def _fetch_raw_utf8(self, repo_id: str, branch: str, relative_path: str) -> str | None:
        """GET a UTF-8 text file from ``raw.githubusercontent.com`` for ``org/repo@branch/relative_path``."""
        rel_err = _validate_repo_relative_path(relative_path)
        if rel_err:
            return None
        rel = relative_path.lstrip("/")
        raw_path = "/".join(urllib.parse.quote(seg, safe="") for seg in (self.org, repo_id, branch, rel))
        url = f"{RAW}/{raw_path}"
        body = self._http_bytes(url)
        return body.decode("utf-8") if body is not None else None

    def _clear_caches(self) -> None:
        self._repo_access_cache: dict[str, RepoAccess] = {}
        self._pre_commit_cache: dict[str, tuple[str | None, str | None]] = {}
        self._file_cache: dict[tuple[str, str], str | None] = {}

    def _http_json(self, url: str) -> Any:
        _assert_https_github_url(url)
        resp = self._session.get(url, timeout=45)
        resp.raise_for_status()
        return resp.json()

    def _http_bytes(self, url: str) -> bytes | None:
        _assert_https_github_url(url)
        resp = self._session.get(url, timeout=45)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        body = resp.content
        if not isinstance(body, bytes):
            msg = f"expected HTTP response body as bytes, got {type(body).__name__}"
            raise TypeError(msg)
        return body

    def get_repo_access(self, repo_id: str) -> RepoAccess:
        """Whether the repository exists and is visible to the API; default branch when ok."""
        if repo_id in self._repo_access_cache:
            return self._repo_access_cache[repo_id]
        rid_err = github_repo_id_error(repo_id)
        if rid_err:
            result = RepoAccess(False, None, f"Invalid repository id: {rid_err}", None)
            self._repo_access_cache[repo_id] = result
            return result
        api_path = f"/repos/{urllib.parse.quote(self.org)}/{urllib.parse.quote(repo_id)}"
        url = f"{GITHUB_API}{api_path}"
        try:
            data = self._http_json(url)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else None
            slug = f"{self.org}/{repo_id}"
            if code == 404:
                result = RepoAccess(
                    False,
                    None,
                    f"GitHub API returned 404 for {slug} (repository not found or not visible "
                    "with the current credentials).",
                    404,
                )
            elif code == 403:
                result = RepoAccess(
                    False,
                    None,
                    f"GitHub API returned 403 for {slug} (access forbidden; the repository may be "
                    "private—use a token with appropriate scope).",
                    403,
                )
            elif code == 401:
                result = RepoAccess(
                    False,
                    None,
                    "GitHub API returned 401 (invalid or missing authentication token).",
                    401,
                )
            elif code == 429:
                result = RepoAccess(
                    False,
                    None,
                    "GitHub API returned 429 (rate limited). Set GITHUB_TOKEN or wait and retry.",
                    429,
                )
            else:
                raise
            self._repo_access_cache[repo_id] = result
            return result
        except requests.RequestException as e:
            result = RepoAccess(
                False,
                None,
                f"GitHub API request failed ({type(e).__name__}): {e}",
                None,
            )
            self._repo_access_cache[repo_id] = result
            return result
        if not isinstance(data, dict):
            result = RepoAccess(
                False,
                None,
                f"Unexpected GitHub API response for {self.org}/{repo_id}: expected a JSON object.",
                None,
            )
            self._repo_access_cache[repo_id] = result
            return result
        branch = data.get("default_branch")
        b = branch if isinstance(branch, str) and branch else "main"
        result = RepoAccess(True, b, None, None)
        self._repo_access_cache[repo_id] = result
        return result

    def fetch_pre_commit_config(self, repo_id: str) -> tuple[str | None, str | None]:
        """Return ``(filename, yaml_text)`` or ``(None, None)`` if no config file exists."""
        if repo_id in self._pre_commit_cache:
            return self._pre_commit_cache[repo_id]
        missing: tuple[str | None, str | None] = (None, None)
        branch = self._validated_default_branch(repo_id)
        if branch is None:
            self._pre_commit_cache[repo_id] = missing
            return missing
        for name in PRE_COMMIT_FILENAMES:
            text = self._fetch_raw_utf8(repo_id, branch, name)
            if text is not None:
                result = (name, text)
                self._pre_commit_cache[repo_id] = result
                return result
        self._pre_commit_cache[repo_id] = missing
        return missing

    def fetch_repo_text_file(self, repo_id: str, relative_path: str) -> str | None:
        key = (repo_id, relative_path.lstrip("/"))
        if key in self._file_cache:
            return self._file_cache[key]
        branch = self._validated_default_branch(repo_id)
        if branch is None:
            self._file_cache[key] = None
            return None
        text = self._fetch_raw_utf8(repo_id, branch, relative_path)
        self._file_cache[key] = text
        return text


# ---------------------------------------------------------------------------
# URL → owner/repo
# ---------------------------------------------------------------------------


class GitHubRepoSlug:
    """Parse ``owner/name`` from a pre-commit ``repo`` URL field."""

    @staticmethod
    def parse(repo_field: str) -> str | None:
        s = repo_field.strip().rstrip("/")
        if s.endswith(".git"):
            s = s[:-4]
        if s.startswith("git@github.com:"):
            path = s.split(":", 1)[1].strip().rstrip("/")
            if path.endswith(".git"):
                path = path[:-4]
            parts = path.split("/")
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
            return None
        _before, sep, after = s.partition("github.com/")
        if sep:
            rest = after.strip("/").split("/")
            if len(rest) >= 2:
                return f"{rest[0]}/{rest[1]}"
        return None


# ---------------------------------------------------------------------------
# additional_dependencies pinning heuristics
# ---------------------------------------------------------------------------


class AdditionalDependencyPinning:
    """Decides whether a dependency string looks version- or URL-pinned.

    Python / PEP 508 hooks typically use ``package==1.2.3``. NPM-style specs put the version after
    the last ``@``: unscoped ``eslint@8.57.0`` or scoped ``@typescript-eslint/eslint-plugin@6.0.0``.
    We treat NPM specs as pinned only when that trailing segment is an exact version (no semver
    range operators). ``git@github.com:…`` SSH URLs and `` @ `` (PEP 508 URL markers) are ignored so
    we do not mis-detect them as NPM.
    """

    # Exact release-ish tail: optional leading "v", numeric semver core, optional pre-release/build.
    _NPM_EXACT_VERSION_RE = re.compile(
        r"v?\d+(?:\.\d+)*(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",
        re.I,
    )

    @classmethod
    def _npm_exact_version_tail(cls, tail: str) -> bool:
        """True when ``tail`` is the version segment after ``@`` and looks like a single version, not a range."""
        t = tail.strip()
        if not t:
            return False
        if t[0] in "^~><=":
            return False
        return cls._NPM_EXACT_VERSION_RE.fullmatch(t) is not None

    @classmethod
    def _npm_package_at_version(cls, spec: str) -> bool:
        """True for ``name@exact`` or ``@scope/name@exact`` NPM dependency strings (not ranges)."""
        if "@" not in spec or " @ " in spec:
            return False
        if spec.startswith("git@"):
            return False
        head, sep, tail = spec.rpartition("@")
        if sep != "@" or not tail or not cls._npm_exact_version_tail(tail):
            return False
        if not head.startswith("@"):
            return bool(head.strip())
        return "/" in head and head.count("@") == 1

    @classmethod
    def is_pinned(cls, spec: str) -> bool:
        t = spec.strip()
        if not t:
            return False
        tl = t.lower()
        return any(
            (
                "==" in t,
                tl.startswith(("git+", "hg+", "bzr+", "svn+")),
                "file:" in tl,
                " @ " in t,
                cls._npm_package_at_version(t),
                "://" in t,
            ),
        )


# ---------------------------------------------------------------------------
# Parsed pre-commit config
# ---------------------------------------------------------------------------


class PreCommitConfigDocument:
    """In-memory ``repos:`` / ``hooks:`` structure from ``.pre-commit-config.yaml``."""

    __slots__ = ("_data",)

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @classmethod
    def try_parse(cls, text: str) -> tuple[PreCommitConfigDocument | None, str | None]:
        """Return ``(document, None)`` or ``(None, error_detail)``."""
        try:
            raw = yaml.safe_load(text)
        except yaml.YAMLError as e:
            return None, str(e)
        if not isinstance(raw, dict):
            return None, f"expected mapping at root, got {type(raw).__name__}"
        return cls(raw), None

    def iter_repo_hooks(self) -> Iterator[tuple[Any, dict[str, Any]]]:
        """Yield ``(repo_field, hook)`` with the raw YAML ``repo`` value (may not be a string)."""
        repos_list = self._data.get("repos")
        if not isinstance(repos_list, list):
            return
        for repo_entry in repos_list:
            if not isinstance(repo_entry, dict):
                continue
            repo_field = repo_entry.get("repo", "")
            hooks = repo_entry.get("hooks")
            if not isinstance(hooks, list):
                continue
            for hook in hooks:
                if isinstance(hook, dict):
                    yield repo_field, hook

    @staticmethod
    def _repo_label(repo_field: Any) -> str:
        return repo_field.strip() if isinstance(repo_field, str) else repr(repo_field)

    @staticmethod
    def _hook_id(hook: dict[str, Any]) -> str:
        hid = hook.get("id")
        if isinstance(hid, str) and hid.strip():
            return hid.strip()
        return "<no id>"

    def _hooks_nonempty_additional_dependencies(
        self,
    ) -> Iterator[tuple[str, str, list[Any] | None, dict[str, Any]]]:
        """Yield ``(repo_label, hook_id, deps_or_none, hook)`` for hooks that declare the key.

        ``deps_or_none`` is ``None`` when ``additional_dependencies`` is not a YAML list.
        """
        for repo_field, hook in self.iter_repo_hooks():
            raw = hook.get("additional_dependencies")
            if raw is None:
                continue
            label = self._repo_label(repo_field)
            hid = self._hook_id(hook)
            if not isinstance(raw, list):
                yield label, hid, None, hook
                continue
            if len(raw) == 0:
                continue
            yield label, hid, raw, hook

    def additional_dependencies_language_issues(self) -> list[str]:
        """Human-readable partial lines for hooks that break the language / shape rules."""
        issues: list[str] = []
        for label, hid, ad, hook in self._hooks_nonempty_additional_dependencies():
            if ad is None:
                bad = hook.get("additional_dependencies")
                issues.append(
                    f"repo {label}, id {hid}: additional_dependencies must be a list, not {type(bad).__name__}",
                )
                continue
            lang = hook.get("language")
            if lang is None:
                issues.append(f"repo {label}, id {hid}")
                continue
            if isinstance(lang, str):
                if not lang.strip():
                    issues.append(f"repo {label}, id {hid}")
                continue
            issues.append(
                f"repo {label}, id {hid}: language must be a non-empty string, not {type(lang).__name__}",
            )
        return issues

    def unpinned_additional_dependency_issues(self) -> list[str]:
        """Human-readable partial lines for unpinned or malformed ``additional_dependencies``."""
        issues: list[str] = []
        for label, hid, ad, hook in self._hooks_nonempty_additional_dependencies():
            if ad is None:
                bad = hook.get("additional_dependencies")
                issues.append(
                    f"repo {label}, id {hid}: additional_dependencies must be a list, not {type(bad).__name__}",
                )
                continue
            for dep in ad:
                spec = dep if isinstance(dep, str) else repr(dep)
                if not AdditionalDependencyPinning.is_pinned(spec):
                    issues.append(f"repo {label}, id {hid}, dependency {spec}")
        return issues


@dataclass(frozen=True)
class CanonicalPreCommitHookPolicy:
    """Require a given hook id to come from a specific ``owner/name`` on GitHub."""

    hook_id: str
    github_owner_repo: str

    def expected_url(self) -> str:
        return f"https://github.com/{self.github_owner_repo}"

    @staticmethod
    def _hook_display_id(hook: dict[str, Any]) -> str:
        hid = hook.get("id")
        if isinstance(hid, str) and hid.strip():
            return hid.strip()
        return "<no id>"

    def violations(self, doc: PreCommitConfigDocument) -> list[str] | None:
        """``None`` if satisfied; if not, a (possibly empty) list of partial lines for each problem."""
        found_canonical = False
        partials: list[str] = []
        for repo_field, hook in doc.iter_repo_hooks():
            if hook.get("id") != self.hook_id:
                continue
            hid = self._hook_display_id(hook)
            if not isinstance(repo_field, str):
                partials.append(f"id {hid}: repository entry is not a string ({type(repo_field).__name__})")
                continue
            slug = GitHubRepoSlug.parse(repo_field)
            if slug == self.github_owner_repo:
                found_canonical = True
            else:
                partials.append(f"repo {repo_field}, id {hid}")
        if found_canonical:
            return None
        if partials:
            return partials
        return []


ZIZMOR_POLICY = CanonicalPreCommitHookPolicy("zizmor", "woodruffw/zizmor-pre-commit")
RENOVATE_VALIDATOR_POLICY = CanonicalPreCommitHookPolicy(
    "renovate-config-validator",
    "renovatebot/pre-commit-hooks",
)


# ---------------------------------------------------------------------------
# renovate.json
# ---------------------------------------------------------------------------


class RenovateConfigRules:
    """Rules for ``renovate.json`` ``extends``."""

    @staticmethod
    def extends_entries(data: dict[str, Any]) -> list[str]:
        ext = data.get("extends")
        if ext is None:
            return []
        if isinstance(ext, str):
            return [ext.strip()] if ext.strip() else []
        if isinstance(ext, list):
            return [str(x).strip() for x in ext if isinstance(x, str) and x.strip()]
        return []

    @classmethod
    def extends_violations(cls, data: dict[str, Any], required: str) -> list[str]:
        extends = cls.extends_entries(data)
        if required in extends:
            return []
        if not extends:
            return ["missing or empty extends"]
        return [f"extends is {extends!r}"]


# ---------------------------------------------------------------------------
# Deployment documentation (README section or docs/DEPLOY.md)
# ---------------------------------------------------------------------------


def deployment_audit_today() -> date:
    """UTC calendar date used for ``last_review`` freshness (overridable in tests)."""

    return datetime.now(timezone.utc).date()


class DeploymentDocumentationRules:
    """Require either a ``Deployment`` README heading or ``docs/DEPLOY.md``.

    Each satisfied source must use a ``Deployment`` heading (ATX or setext). The first line
    with content after that heading must be only ``<!-- last_review: YYYY-MM-DD -->``, dated
    within the last 365 days (UTC).
    """

    _DEPLOYMENT_HEADING_NORMALIZED = "deployment"
    _LAST_REVIEW_FULL_LINE_RE = re.compile(
        r"^<!--\s*last_review\s*:\s*(\d{4}-\d{2}-\d{2})\s*-->$",
        re.IGNORECASE,
    )
    _LAST_REVIEW_MAX_AGE = timedelta(days=365)

    @classmethod
    def readme_has_deployment_heading(cls, readme: str) -> bool:
        """True if the readme has an ATX or setext heading titled *deployment* (case-insensitive)."""
        if cls._readme_atx_has_deployment(readme):
            return True
        return cls._readme_setext_has_deployment(readme)

    @staticmethod
    def _normalize_heading_title(raw: str) -> str:
        t = re.sub(r"\s+#+\s*$", "", raw.strip()).strip()
        t = re.sub(r"[*_`]+", "", t).strip()
        return t.casefold()

    @classmethod
    def _readme_atx_has_deployment(cls, readme: str) -> bool:
        for line in readme.splitlines():
            s = line.lstrip()
            if not s.startswith("#"):
                continue
            hashes = 0
            for c in s:
                if c == "#":
                    hashes += 1
                else:
                    break
            if hashes > 6 or hashes < 1:
                continue
            rest = s[hashes:]
            if not rest.startswith(" "):
                continue
            title = cls._normalize_heading_title(rest)
            if title == cls._DEPLOYMENT_HEADING_NORMALIZED:
                return True
        return False

    @classmethod
    def _readme_setext_has_deployment(cls, readme: str) -> bool:
        lines = readme.splitlines()
        for i, line in enumerate(lines[:-1]):
            if line.strip().casefold() != cls._DEPLOYMENT_HEADING_NORMALIZED:
                continue
            underline = lines[i + 1].strip()
            if len(underline) < 3:
                continue
            if set(underline) <= {"="} or set(underline) <= {"-"}:
                return True
        return False

    @classmethod
    def _content_start_index_after_first_deployment_heading(cls, lines: list[str]) -> int | None:
        """Index of the first line after the opening ``Deployment`` heading (ATX or setext), or ``None``."""

        n = len(lines)
        i = 0
        while i < n:
            s = lines[i].lstrip()
            if s.startswith("#"):
                hashes = 0
                for c in s:
                    if c == "#":
                        hashes += 1
                    else:
                        break
                if 1 <= hashes <= 6:
                    rest = s[hashes:]
                    if rest.startswith(" "):
                        title = cls._normalize_heading_title(rest)
                        if title == cls._DEPLOYMENT_HEADING_NORMALIZED:
                            return i + 1
            if i + 1 < n and lines[i].strip().casefold() == cls._DEPLOYMENT_HEADING_NORMALIZED:
                underline = lines[i + 1].strip()
                if len(underline) >= 3 and (set(underline) <= {"="} or set(underline) <= {"-"}):
                    return i + 2
            i += 1
        return None

    @classmethod
    def last_review_after_deployment_heading_violation(
        cls,
        text: str,
        *,
        source_label: str,
        today: date | None = None,
    ) -> str | None:
        """Return a violation string, or ``None`` if placement and date are valid."""

        lines = text.splitlines()
        start = cls._content_start_index_after_first_deployment_heading(lines)
        if start is None:
            return f'{source_label}: no heading titled "Deployment"'

        first_content: str | None = None
        for j in range(start, len(lines)):
            stripped = lines[j].strip()
            if stripped:
                first_content = stripped
                break
        if first_content is None:
            return (
                f"{source_label}: first line with content after the Deployment heading must be "
                "<!-- last_review: YYYY-MM-DD --> (no content after heading)"
            )

        m = cls._LAST_REVIEW_FULL_LINE_RE.match(first_content)
        if not m:
            return (
                f"{source_label}: first line with content after the Deployment heading must be "
                f"only <!-- last_review: YYYY-MM-DD --> (got {first_content!r})"
            )

        raw = m.group(1)
        try:
            parsed = date.fromisoformat(raw)
        except ValueError:
            return f"{source_label}: invalid last_review date {raw!r} (use YYYY-MM-DD)"

        ref = today if today is not None else deployment_audit_today()
        if ref - parsed > cls._LAST_REVIEW_MAX_AGE:
            cutoff = ref - cls._LAST_REVIEW_MAX_AGE
            return (
                f"{source_label}: last_review {parsed.isoformat()} is older than one year "
                f"(must be on or after {cutoff.isoformat()}, UTC)"
            )
        return None


# ---------------------------------------------------------------------------
# Audit flow
# ---------------------------------------------------------------------------


class AuditLog:
    """Builds per-repo log lines: ``FAIL`` always; ``PASS`` and ``SKIP`` only when verbose."""

    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.lines: list[str] = []

    def record_skip(self, label: str, reason: str) -> None:
        """Record that a check did not apply (only emitted when ``verbose`` is true)."""
        if self.verbose:
            self.lines.append(f"{label}: SKIP ({reason})")

    def record_check(
        self,
        label: str,
        ok: bool,
        *,
        partial_messages: Sequence[str] | None = None,
    ) -> None:
        """Record one audit outcome. No extra text on the PASS/FAIL line; use ``partial_messages`` for detail."""
        if ok:
            if self.verbose:
                self.lines.append(f"{label}: PASS")
            return
        self.lines.append(f"{label}: FAIL")
        for msg in partial_messages or []:
            text = msg.strip()
            if text:
                self.lines.append(f"  {text}")


@dataclass
class AuditContext:
    """Lazy state for auditing a single GitHub repo."""

    client: GitHubRepoClient
    repo: dict[str, Any]
    log: AuditLog
    _pre_commit_raw: tuple[str | None, str | None] | None = field(default=None, init=False, repr=False)
    _pre_commit_parse: tuple[PreCommitConfigDocument | None, str | None] | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _renovate_json_fetched: bool = field(default=False, init=False, repr=False)
    _renovate_json_text: str | None = field(default=None, init=False, repr=False)
    _readme_for_deployment_audit_fetched: bool = field(default=False, init=False, repr=False)
    _readme_for_deployment_audit_text: str | None = field(default=None, init=False, repr=False)
    _deploy_md_fetched: bool = field(default=False, init=False, repr=False)
    _deploy_md_text: str | None = field(default=None, init=False, repr=False)
    _release_yml_fetched: bool = field(default=False, init=False, repr=False)
    _release_yml_text: str | None = field(default=None, init=False, repr=False)

    @property
    def repo_id(self) -> str:
        rid = self.repo["id"]
        if not isinstance(rid, str) or not rid.strip():
            msg = f"repositories.json entry must have a non-empty string 'id', got {type(rid).__name__}"
            raise TypeError(msg)
        s = rid.strip()
        rid_err = github_repo_id_error(s)
        if rid_err:
            msg = f"Invalid repository id {s!r}: {rid_err}"
            raise ValueError(msg)
        return s

    def pre_commit_raw(self) -> tuple[str | None, str | None]:
        if self._pre_commit_raw is None:
            self._pre_commit_raw = self.client.fetch_pre_commit_config(self.repo_id)
        return self._pre_commit_raw

    def pre_commit_parse(self) -> tuple[PreCommitConfigDocument | None, str | None]:
        """``(doc, None)``, ``(None, yaml_error)``, or ``(None, None)`` if no file."""
        if self._pre_commit_parse is not None:
            return self._pre_commit_parse
        path, text = self.pre_commit_raw()
        if path is None or text is None:
            self._pre_commit_parse = (None, None)
            return self._pre_commit_parse
        self._pre_commit_parse = PreCommitConfigDocument.try_parse(text)
        return self._pre_commit_parse

    def pre_commit_document(self) -> PreCommitConfigDocument | None:
        doc, _err = self.pre_commit_parse()
        return doc

    def renovate_json_text(self) -> str | None:
        if not self._renovate_json_fetched:
            self._renovate_json_text = self.client.fetch_repo_text_file(self.repo_id, RENOVATE_JSON_FILE)
            self._renovate_json_fetched = True
        return self._renovate_json_text

    def readme_text_for_deployment_audit(self) -> str | None:
        """First available readme body among :data:`README_FILENAMES_FOR_DEPLOYMENT_AUDIT`, or ``None``."""
        if not self._readme_for_deployment_audit_fetched:
            text: str | None = None
            for name in README_FILENAMES_FOR_DEPLOYMENT_AUDIT:
                text = self.client.fetch_repo_text_file(self.repo_id, name)
                if text is not None:
                    break
            self._readme_for_deployment_audit_text = text
            self._readme_for_deployment_audit_fetched = True
        return self._readme_for_deployment_audit_text

    def deploy_md_text(self) -> str | None:
        if not self._deploy_md_fetched:
            self._deploy_md_text = self.client.fetch_repo_text_file(self.repo_id, DEPLOY_MD_RELATIVE_PATH)
            self._deploy_md_fetched = True
        return self._deploy_md_text

    def release_yml_text(self) -> str | None:
        if not self._release_yml_fetched:
            self._release_yml_text = self.client.fetch_repo_text_file(self.repo_id, RELEASE_YML_RELATIVE_PATH)
            self._release_yml_fetched = True
        return self._release_yml_text


class AuditCheck(ABC):
    """One policy check against a repository."""

    @property
    @abstractmethod
    def summary_label(self) -> str:
        """What this check verifies (used in log lines and end-of-run failure counts)."""

    @abstractmethod
    def run(self, ctx: AuditContext) -> bool:
        """Return ``True`` if the check passed.

        Before returning, call :meth:`AuditLog.record_check` or :meth:`AuditLog.record_skip`
        so verbose mode prints one outcome line per check (PASS, FAIL, or SKIP).
        """


class GitHubRepoAccessibleCheck(AuditCheck):
    """Ensure ``GET /repos/{org}/{repo}`` succeeds before reading files from the repo."""

    @property
    def summary_label(self) -> str:
        return "GitHub repository is reachable via the API"

    def run(self, ctx: AuditContext) -> bool:
        access = ctx.client.get_repo_access(ctx.repo_id)
        if access.ok:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(
            self.summary_label,
            False,
            partial_messages=[access.block_reason or "unknown error"],
        )
        return False


class PreCommitFileExistsCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return "Pre-commit config file exists on the default branch"

    def run(self, ctx: AuditContext) -> bool:
        path, _text = ctx.pre_commit_raw()
        if path:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False)
        return False


class PreCommitYamlValidCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return "Pre-commit config is valid YAML with a mapping root"

    def run(self, ctx: AuditContext) -> bool:
        path, _text = ctx.pre_commit_raw()
        if path is None:
            ctx.log.record_skip(
                self.summary_label,
                "no pre-commit configuration file on the default branch",
            )
            return True
        doc, err = ctx.pre_commit_parse()
        if doc is not None:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(
            self.summary_label,
            False,
            partial_messages=[err or "unknown parse error"],
        )
        return False


class AdditionalDepsLanguageCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return "Pre-commit sets language on hooks that use additional_dependencies"

    def run(self, ctx: AuditContext) -> bool:
        doc = ctx.pre_commit_document()
        if doc is None:
            ctx.log.record_skip(
                self.summary_label,
                "no pre-commit configuration file or YAML could not be parsed",
            )
            return True
        issues = doc.additional_dependencies_language_issues()
        if not issues:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False, partial_messages=issues)
        return False


class AdditionalDepsPinnedCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return "Pre-commit pins each additional_dependencies entry"

    def run(self, ctx: AuditContext) -> bool:
        doc = ctx.pre_commit_document()
        if doc is None:
            ctx.log.record_skip(
                self.summary_label,
                "no pre-commit configuration file or YAML could not be parsed",
            )
            return True
        issues = doc.unpinned_additional_dependency_issues()
        if not issues:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False, partial_messages=sorted(issues))
        return False


class CanonicalPreCommitHookCheck(AuditCheck):
    """Enforce :class:`CanonicalPreCommitHookPolicy` (zizmor, renovate validator, …)."""

    def __init__(self, policy: CanonicalPreCommitHookPolicy, summary_label: str) -> None:
        self._policy = policy
        self._summary_label = summary_label

    @property
    def summary_label(self) -> str:
        return self._summary_label

    def run(self, ctx: AuditContext) -> bool:
        doc = ctx.pre_commit_document()
        if doc is None:
            ctx.log.record_skip(
                self.summary_label,
                "no pre-commit configuration file or YAML could not be parsed",
            )
            return True
        errors = self._policy.violations(doc)
        if errors is None:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False, partial_messages=errors)
        return False


class RenovateJsonPresentCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return "renovate.json exists on the default branch"

    def run(self, ctx: AuditContext) -> bool:
        text = ctx.renovate_json_text()
        if text is not None:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False)
        return False


class RenovateExtendsCheck(AuditCheck):
    @property
    def summary_label(self) -> str:
        return f"renovate.json extends {RENOVATE_EXTENDS_REQUIRED!r}"

    def run(self, ctx: AuditContext) -> bool:
        text = ctx.renovate_json_text()
        if text is None:
            ctx.log.record_check(
                self.summary_label,
                False,
                partial_messages=["renovate.json not on the default branch (cannot verify extends)"],
            )
            return False
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            ctx.log.record_check(
                self.summary_label,
                False,
                partial_messages=[f"invalid JSON: {e}"],
            )
            return False
        if not isinstance(data, dict):
            ctx.log.record_check(
                self.summary_label,
                False,
                partial_messages=[f"root must be a JSON object, not {type(data).__name__}"],
            )
            return False
        violations = RenovateConfigRules.extends_violations(data, RENOVATE_EXTENDS_REQUIRED)
        if not violations:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False, partial_messages=violations)
        return False


class ReleaseYmlConfigRules:
    """Shape rules for GitHub ``.github/release.yml`` (auto-generated release notes)."""

    @staticmethod
    def _load_root_mapping(text: str) -> tuple[dict[str, Any] | None, list[str]]:
        try:
            raw = yaml.safe_load(text)
        except yaml.YAMLError as e:
            return None, [str(e)]
        if raw is None:
            return None, ["file is empty or YAML resolves to null"]
        if not isinstance(raw, dict):
            return None, [f"root must be a mapping, got {type(raw).__name__}"]
        return raw, []

    @staticmethod
    def _changelog_categories_list(root: dict[str, Any]) -> tuple[list[Any] | None, list[str]]:
        ch = root.get("changelog")
        if ch is None:
            return None, ["missing top-level 'changelog' key"]
        if not isinstance(ch, dict):
            return None, [f"'changelog' must be a mapping, got {type(ch).__name__}"]
        cats = ch.get("categories")
        if cats is None:
            return None, ["changelog.categories is missing"]
        if not isinstance(cats, list):
            return None, [f"changelog.categories must be a list, got {type(cats).__name__}"]
        if len(cats) == 0:
            return None, ["changelog.categories must not be empty"]
        return cats, []

    @staticmethod
    def _single_category_errors(cat: Any, index: int) -> list[str]:
        prefix = f"changelog.categories[{index}]"
        if not isinstance(cat, dict):
            return [f"{prefix} must be a mapping, got {type(cat).__name__}"]
        errors: list[str] = []
        title = cat.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{prefix} needs a non-empty string 'title'")
        labels = cat.get("labels")
        if not isinstance(labels, list) or len(labels) == 0:
            errors.append(f"{prefix} needs a non-empty list 'labels'")
            return errors
        for j, lab in enumerate(labels):
            if not isinstance(lab, str) or not lab.strip():
                errors.append(f"{prefix}.labels[{j}] must be a non-empty string")
        return errors

    @classmethod
    def validation_errors(cls, text: str) -> list[str]:
        """Return human-readable issues, or an empty list when the config looks usable."""
        root, head_errors = cls._load_root_mapping(text)
        if root is None:
            return head_errors
        categories, changelog_errors = cls._changelog_categories_list(root)
        if categories is None:
            return changelog_errors
        out: list[str] = []
        for i, cat in enumerate(categories):
            out.extend(cls._single_category_errors(cat, i))
        return out


class ReleaseYmlCheck(AuditCheck):
    """Require ``.github/release.yml`` unless the repo is marked ``hide_releases`` in ``repositories.json``."""

    @property
    def summary_label(self) -> str:
        return (
            ".github/release.yml exists on the default branch and is valid GitHub release-notes config "
            "(changelog.categories with title and labels)"
        )

    def run(self, ctx: AuditContext) -> bool:
        if ctx.repo.get("hide_releases") is True:
            ctx.log.record_skip(
                self.summary_label,
                "repositories.json sets hide_releases for this repository",
            )
            return True
        text = ctx.release_yml_text()
        if text is None:
            ctx.log.record_check(
                self.summary_label,
                False,
                partial_messages=[f"{RELEASE_YML_RELATIVE_PATH} not found on the default branch"],
            )
            return False
        issues = ReleaseYmlConfigRules.validation_errors(text)
        if not issues:
            ctx.log.record_check(self.summary_label, True)
            return True
        ctx.log.record_check(self.summary_label, False, partial_messages=issues)
        return False


class DeploymentDocumentationCheck(AuditCheck):
    """README or ``docs/DEPLOY.md`` with ``Deployment`` heading and ``last_review`` on the next content line."""

    @property
    def summary_label(self) -> str:
        return (
            'Deployment docs: README "Deployment" or docs/DEPLOY.md, each with '
            "<!-- last_review: YYYY-MM-DD --> as the first content line after that heading, "
            "within the last year (UTC)"
        )

    def run(self, ctx: AuditContext) -> bool:
        readme = ctx.readme_text_for_deployment_audit()
        deploy_md = ctx.deploy_md_text()
        readme_ok = readme is not None and DeploymentDocumentationRules.readme_has_deployment_heading(readme)
        deploy_file_ok = deploy_md is not None
        if not readme_ok and not deploy_file_ok:
            partials: list[str] = []
            if readme is None:
                partials.append("no README.md or readme.md on default branch")
            else:
                partials.append('README has no heading titled "Deployment"')
            if deploy_md is None:
                partials.append(f"no {DEPLOY_MD_RELATIVE_PATH} on default branch")
            ctx.log.record_check(self.summary_label, False, partial_messages=partials)
            return False

        partials: list[str] = []
        if readme_ok and readme is not None:
            v = DeploymentDocumentationRules.last_review_after_deployment_heading_violation(
                readme,
                source_label="README",
            )
            if v:
                partials.append(v)
        if deploy_file_ok and deploy_md is not None:
            if not DeploymentDocumentationRules.readme_has_deployment_heading(deploy_md):
                partials.append(
                    f'{DEPLOY_MD_RELATIVE_PATH}: no heading titled "Deployment" '
                    "(required when this file is present; place <!-- last_review: YYYY-MM-DD --> "
                    "on the first line with content after that heading)",
                )
            else:
                v = DeploymentDocumentationRules.last_review_after_deployment_heading_violation(
                    deploy_md,
                    source_label=DEPLOY_MD_RELATIVE_PATH,
                )
                if v:
                    partials.append(v)
        if partials:
            ctx.log.record_check(self.summary_label, False, partial_messages=partials)
            return False
        ctx.log.record_check(self.summary_label, True)
        return True


def default_audit_checks() -> list[AuditCheck]:
    """Standard suite, in run order."""
    return [
        GitHubRepoAccessibleCheck(),
        PreCommitFileExistsCheck(),
        PreCommitYamlValidCheck(),
        AdditionalDepsLanguageCheck(),
        AdditionalDepsPinnedCheck(),
        CanonicalPreCommitHookCheck(
            ZIZMOR_POLICY,
            "Pre-commit registers zizmor from woodruffw/zizmor-pre-commit",
        ),
        # Renovate: file must exist before we assert extends (both fail if the file is missing).
        RenovateJsonPresentCheck(),
        RenovateExtendsCheck(),
        ReleaseYmlCheck(),
        DeploymentDocumentationCheck(),
        CanonicalPreCommitHookCheck(
            RENOVATE_VALIDATOR_POLICY,
            "Pre-commit registers renovate-config-validator from renovatebot/pre-commit-hooks",
        ),
    ]


class RepositoryConfigAudit:
    """Runs :class:`AuditCheck` instances across repositories using one :class:`GitHubRepoClient`."""

    def __init__(self, client: GitHubRepoClient, checks: Sequence[AuditCheck] | None = None) -> None:
        self.client = client
        self.checks: list[AuditCheck] = list(checks) if checks is not None else default_audit_checks()

    def audit_one_repo(self, repo: dict[str, Any], verbose: bool) -> tuple[bool, list[str], list[str]]:
        """Return ``(all_passed, log_lines, summary_labels_for_failed_checks)``."""
        log = AuditLog(verbose)
        ctx = AuditContext(client=self.client, repo=repo, log=log)
        passed = True
        failed_labels: list[str] = []
        for i, check in enumerate(self.checks):
            if not check.run(ctx):
                passed = False
                failed_labels.append(check.summary_label)
                if isinstance(check, GitHubRepoAccessibleCheck):
                    for remainder in self.checks[i + 1 :]:
                        ctx.log.record_skip(
                            remainder.summary_label,
                            "repository not reachable via the GitHub API",
                        )
                    break
        return passed, log.lines, failed_labels


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit listed GitHub repos for pre-commit, Renovate, and related config.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=(
            "Print every check (PASS, FAIL, or SKIP) for each repository. "
            "SKIP means the check did not apply (for example, no pre-commit file)."
        ),
    )
    parser.add_argument(
        "--token",
        metavar="TOKEN",
        default=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
        help=(
            "GitHub personal access token for API and raw requests (reduces rate limiting). "
            "Default: GITHUB_TOKEN or GH_TOKEN. Prefer env over this flag so the token is not visible in process listings."
        ),
    )
    return parser.parse_args(argv)


def _run_audits(
    auditor: RepositoryConfigAudit,
    repos: list[dict[str, Any]],
    verbose: bool,
) -> tuple[int | None, bool, Counter[str], list[tuple[str, bool, int]]]:
    """Return ``(exit_code_if_fatal, any_failed, failure_counts, repo_outcomes)``.

    Each ``repo_outcomes`` entry is ``(display_id, all_checks_passed, num_failed_checks)``.
    """
    failure_counts: Counter[str] = Counter()
    any_failed = False
    repo_outcomes: list[tuple[str, bool, int]] = []
    for index, repo in enumerate(repos):
        try:
            display_id = repository_entry_id(repo, index)
        except ValueError as e:
            print(f"Invalid repositories.json: {e}", file=sys.stderr)
            return 2, False, failure_counts, []
        try:
            passed, lines, failed_labels = auditor.audit_one_repo(repo, verbose)
        except (TypeError, ValueError, requests.RequestException) as e:
            print(f"Error auditing repositories.json entry #{index}: {e}", file=sys.stderr)
            return 2, False, failure_counts, []
        n_failed = len(failed_labels)
        repo_outcomes.append((display_id, passed, n_failed))
        if not passed:
            any_failed = True
            failure_counts.update(failed_labels)
        if verbose or not passed:
            print(display_id)
            for line in lines:
                print(f"  {line}")
            print()
    return None, any_failed, failure_counts, repo_outcomes


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    verbose: bool = args.verbose
    token: str | None = args.token if isinstance(args.token, str) and args.token.strip() else None

    client = GitHubRepoClient(token=token)
    auditor = RepositoryConfigAudit(client)

    repos = load_repositories()
    n_repos = len(repos)
    print(f"Auditing {n_repos} repositories under {OWNER}/…\n")

    fatal, any_failed, failure_counts, repo_outcomes = _run_audits(auditor, repos, verbose)
    if fatal is not None:
        return fatal

    if not verbose and not any_failed:
        print("All repositories passed.")

    summary_rows: list[tuple[str, int]] = []
    for check in auditor.checks:
        label = check.summary_label
        n = failure_counts[label]
        if verbose or n > 0:
            summary_rows.append((label, n))
    if summary_rows:
        print("Summary (repositories failing each rule):")
        for label, n in summary_rows:
            print(f"  {label}: {n}")
    if repo_outcomes:
        print()
        print("Repository summary:")
        for rid, passed_repo, n_failed in repo_outcomes:
            if passed_repo:
                print(f"  ✅ {rid}  passed")
            else:
                checks_word = "check" if n_failed == 1 else "checks"
                print(f"  ❌ {rid}  failed ({n_failed} {checks_word})")
    print(f"  (audited {n_repos} repositories)")

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
