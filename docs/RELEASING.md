# Publishing EmDashify

EmDashify releases are published to [PyPI](https://pypi.org/project/emdashify/) with [GitHub Actions](https://github.com/edujbarrios/EmDashify/actions) and PyPI **Trusted Publishing (OIDC)**. No PyPI API token is stored in the repository.

## New releases

1. Update the version in both `pyproject.toml` and `src/emdashify/__init__.py`; never reuse a published version.
2. Add release notes to `CHANGELOG.md` and merge changes into `main` after CI passes.
3. Create a [GitHub Release](https://github.com/edujbarrios/EmDashify/releases/new) tagged `vX.Y.Z` from `main`, with the tag matching the package version.
4. Publishing the release starts `.github/workflows/release.yml`, which tests, builds, validates, and uploads the distribution to PyPI through OIDC.
5. Check the GitHub Actions run and the new PyPI version. To test the install: `python -m pip install --upgrade "emdashify[word]"`.

The already-published versions `0.1.0` and `0.2.0` must not be republished. The workflow skips retrospective releases for those versions.

## Trusted Publisher

| PyPI setting | Value |
| --- | --- |
| Project | `emdashify` |
| GitHub owner | `edujbarrios` |
| Repository | `EmDashify` |
| Workflow | `release.yml` |
| Environment | Leave blank (as configured in the workflow) |

Limit permissions to edit release workflows or create releases. Publishing a GitHub Release uploads a **public** package to PyPI; ordinary pushes and pull requests do not.

More details: [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/).
