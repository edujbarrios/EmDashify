# Releasing EmDashify to PyPI

EmDashify uses GitHub Actions and PyPI **Trusted Publishing (OIDC)**. No PyPI token is stored in GitHub.

## Current status

- **v0.1.0 was successfully published to PyPI on November 5, 2026.**
- [PyPI package](https://pypi.org/project/emdashify/0.1.0/)
- [Successful publishing workflow](https://github.com/edujbarrios/EmDashify/actions/runs/42019913899)
- The first upload was activated by a one-time branch creation because the connected GitHub integration could not create a GitHub Release. The temporary workflow trigger has been removed; subsequent uploads use GitHub Releases.
- **Do not publish v0.1.0 again**: PyPI does not allow replacing uploaded distribution files, and the workflow deliberately skips that historical tag.

## Future releases

1. Increment the version **in both** `pyproject.toml` (`[project].version`) and `src/emdashify/__init__.py` (`__version__`). Use a new version, for example `0.1.1`.
2. Update `CHANGELOG.md` and merge to `main` after tests pass.
3. Optional local build verification:

   ```bash
   python -m pip install --upgrade build twine
   python -m build
   python -m twine check --strict dist/*
   ```

4. Go to [GitHub Releases](https://github.com/edujbarrios/EmDashify/releases/new), create the **new** tag `vX.Y.Z` from `main` (for example, `v0.1.1`), and publish the release.
5. The `release.yml` workflow runs tests, verifies the tag against package metadata, builds wheel and sdist distributions, then uploads them through the existing PyPI Trusted Publisher.
6. Verify the completed workflow, the [PyPI project page](https://pypi.org/project/emdashify/), and installation with `python -m pip install --upgrade emdashify`.

## Trusted Publisher settings

The active publisher should match the following GitHub identity:

| Field | Value |
| --- | --- |
| PyPI project | `emdashify` |
| GitHub owner | `edujbarrios` |
| Repository | `EmDashify` |
| Workflow filename | `release.yml` |
| Environment | Blank (the publish job currently uses no GitHub environment) |

**Security:** Anyone with permission to change the publishing workflow can potentially alter what is uploaded. Limit merge and release privileges. If your plan supports protected environments for private repositories, add an environment to both the workflow and the PyPI publisher configuration, with matching names and suitable protections.

**A GitHub Release publishes to the public PyPI registry even if the GitHub repository is private.** Normal pushes and pull requests do not publish.

References: [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) · [Python Packaging Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
