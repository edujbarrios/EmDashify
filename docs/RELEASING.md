# Publishing EmDashify to PyPI

EmDashify is published using GitHub Actions and PyPI **Trusted Publishing (OIDC)**. No long-lived PyPI token is stored in the repository.

## Published versions

- [v0.1.0](https://pypi.org/project/emdashify/0.1.0/) — initial release.
- [v0.2.0](https://pypi.org/project/emdashify/0.2.0/) — Word `.docx` support, published November 5, 2026. [Successful GitHub workflow](https://github.com/edujbarrios/EmDashify/actions/runs/42022832898).

Both versions were uploaded using a one-time branch-created workflow because the connected GitHub integration could not create GitHub Releases. Those temporary triggers have been **removed**. The workflow skips retrospective releases tagged `v0.1.0` or `v0.2.0` to prevent duplicate uploads.

## Publishing future versions

1. Increment the version in both `pyproject.toml` and `src/emdashify/__init__.py`, e.g. `0.2.1`. Do not reuse an existing PyPI version.
2. Update `CHANGELOG.md`, run tests, and merge the changes into `main`.
3. Optionally validate locally:

   ```bash
   python -m pip install --upgrade build twine
   python -m build
   python -m twine check --strict dist/*
   ```

4. Open [GitHub Releases](https://github.com/edujbarrios/EmDashify/releases/new), create the matching tag (e.g. `v0.2.1`) from `main`, and **Publish release**.
5. `.github/workflows/release.yml` builds, tests, checks the version, and publishes to PyPI through the existing Trusted Publisher.
6. Verify both the [PyPI project page](https://pypi.org/project/emdashify/) and the [GitHub Actions run](https://github.com/edujbarrios/EmDashify/actions). For Word support, install `pip install "emdashify[word]"`.

## Trusted Publisher configuration

| PyPI setting | Value |
| --- | --- |
| Project | `emdashify` |
| GitHub owner | `edujbarrios` |
| Repository | `EmDashify` |
| Workflow filename | `release.yml` |
| Environment | Blank (the publishing job has no environment) |

Keep release and workflow edit permissions limited to maintainers. A package uploaded to **PyPI is public**, even when the GitHub source repository is private.

References: [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/) · [Python Packaging Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
