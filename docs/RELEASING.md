# Releasing EmDashify to PyPI

EmDashify publishes through GitHub Actions using PyPI **Trusted Publishing** (OIDC). No long-lived PyPI API tokens or passwords are stored in GitHub.

## One-time setup (before the first release)

1. Create a [PyPI account](https://pypi.org/account/register/) and enable two-factor authentication.
2. Open [PyPI → Account → Publishing](https://pypi.org/manage/account/publishing/) and add a **pending trusted publisher** for a new project. Enter:

   | Field | Value |
   | --- | --- |
   | PyPI project name | `emdashify` |
   | GitHub owner | `edujbarrios` |
   | Repository | `EmDashify` |
   | Workflow filename | `release.yml` |
   | Environment name | **Leave blank** (this workflow does not use a GitHub environment) |

3. A pending publisher **does not reserve** the name. Confirm that `emdashify` is available on PyPI before publishing.
4. Review `.github/workflows/release.yml` and repository permissions. Only trusted maintainers should be able to create releases or modify the release workflow.

**Optional hardening:** If your GitHub plan supports environments for a private repository, add an environment named `pypi` to the publish job and to the PyPI Trusted Publisher configuration. Configure allowed deployment tags and, if supported, required reviewers. Keep both values identical. Some GitHub plans do not support environments or required reviewers for private repositories; the default workflow does not depend on them.

## Publish a release

1. Update the version in **both** `pyproject.toml` (`[project].version`) and `src/emdashify/__init__.py` (`__version__`).
2. Update `CHANGELOG.md`, run the tests, and merge changes into `main`.
3. Build and validate locally, if desired:

   ```bash
   python -m pip install --upgrade build twine
   python -m build
   python -m twine check dist/*
   ```

4. Open **GitHub → Releases → Draft a new release**. Create a tag **`vX.Y.Z`** from `main` (for example, `v0.1.0`), give the release a title, and click **Publish release**.
5. The `release.yml` workflow verifies the version, runs tests, builds and checks the wheel and source distribution, and submits them to PyPI using Trusted Publishing.
6. Verify `https://pypi.org/project/emdashify/` and install from PyPI:

   ```bash
   python -m pip install emdashify
   emdashify "Hello -- world"
   ```

## Safety notes

- **Publishing a GitHub Release triggers a real PyPI upload.** Do not click Publish release until the PyPI Trusted Publisher is configured and you intend to release.
- A PyPI version cannot be re-uploaded with the same distribution filenames. Increase the version for subsequent releases.
- The tag must match the version in `pyproject.toml`; the workflow fails before publishing if it does not.
- There is no automatic PyPI release on ordinary pushes or pull requests.
- If `emdashify` is unavailable on PyPI, pick another distribution name and update `pyproject.toml`, the project URLs where needed, and the pending Trusted Publisher.

References: [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/), [Python Packaging Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
