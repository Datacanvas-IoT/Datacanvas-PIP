# Contributing

Thank you for contributing to DataCanvas SDK. This document explains how to open PRs, the release process, and how maintainers should publish to PyPI.

## Pull Request Checklist

- [ ] Follow conventional commits for commit messages (e.g. `feat:`, `fix:`, `chore:`).
- [ ] Add or update unit tests for new behaviour when applicable.
- [ ] Update `CHANGELOG.md` — add concise bullets to the `Unreleased` section describing user-visible changes.
- [ ] Ensure `pytest` and `mypy src/datacanvas` pass locally.
- [ ] Ensure CI checks pass and obtain required reviews before merging.

Note: Direct pushes to `main` are restricted — open a PR and request review from maintainers.

## Branching and Releases

- Work in feature branches: `feature/awesome`, `fix/bug-name`.
- Open a PR targeting `main` when ready.

### Release process (maintainers)

1. Increment the `version` field in `pyproject.toml` (semantic versioning).
2. Move `Unreleased` entries in `CHANGELOG.md` into a new heading for the released version and add the release date (YYYY-MM-DD).
3. Commit the version bump and changelog changes on a branch and open a PR to `main`.
4. Once CI passes and required reviews are complete, merge to `main` (branch protection ensures appropriate checks and reviews).
5. The GitHub Action at `.github/workflows/pypi-publish.yml` will run on the push to `main` and publish the package to PyPI using the `PYPI_API_TOKEN` secret.

Important: Be sure the `version` is updated to a previously unpublished value; PyPI will reject publishing an existing version.

## Local development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/datacanvas

# Linting
ruff check src/
```

## Building and publishing locally

To build and publish locally (for maintainers with a PyPI token configured):

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Validate the distribution
twine check dist/*

# Upload to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD or a .pypirc)
twine upload dist/*
```

## Security

- **Never** commit API keys, secrets, or `.env` files to the repository.
- Store sensitive values as GitHub Actions secrets or environment variables.
- The PyPI token must be stored as the `PYPI_API_TOKEN` secret in the repository settings.

## Contact / Support

If you have trouble generating the token or setting secrets, contact the maintainers listed in the README or open an issue.
