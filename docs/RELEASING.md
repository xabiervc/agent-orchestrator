# Releasing

## Pre-release checklist

1. Confirm the CI workflow for `main` is green.
2. Confirm `pyproject.toml` contains the intended version.
3. Run `pytest -q`.
4. Build with `python -m build`.
5. Run `python -m twine check dist/*`.
6. Check the repository for secrets.

## GitHub Release

Create an annotated tag and push it:

```powershell
git checkout main
git pull origin main
git tag -a v0.1.0 -m "Release agent-orchestrator v0.1.0"
git push origin v0.1.0
```

Create a GitHub Release for `v0.1.0` using `RELEASE_NOTES_v0.1.0.md`. Mark it as a pre-release while the API is experimental.

## PyPI Trusted Publishing

Before publishing, configure a PyPI Trusted Publisher for:

- Owner: `xabiervc`
- Repository: `agent-orchestrator`
- Workflow: `publish.yml`
- Environment: `pypi`

The publish workflow is triggered only by a published GitHub Release. It uses GitHub's OIDC identity and does not store a PyPI token in the repository.

If PyPI is not configured yet, publish the GitHub Release first and leave the package workflow disabled or expect its publish job to require configuration. Installing from GitHub remains available:

```powershell
pipx install git+https://github.com/xabiervc/agent-orchestrator.git@v0.1.0
```
