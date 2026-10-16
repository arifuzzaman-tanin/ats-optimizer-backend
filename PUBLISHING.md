# Publish the package

The package uses the Unlicense and is ready for public distribution. Before
publishing, confirm that every bundled catalogue entry is yours to release.

## 1. Test and build

```bash
pip install -e ".[pdf,dev]"
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

## 2. Test on TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

Install the test release:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ats-optimizer
```

## 3. Publish to PyPI

```bash
python -m twine upload dist/*
```

Trusted Publishing through the included GitHub Actions workflow is safer than
storing a PyPI token. Configure the `testpypi` and `pypi` environments in
GitHub, then run the **Package CI and publish** workflow.

Before every release:

- Confirm the `ats-optimizer` name is still available.
- Update the version in `pyproject.toml` and `src/ats_optimizer/__init__.py`.
- Update `CHANGELOG.md`.
- Test the built wheel in a clean environment.
- Never commit passwords or PyPI tokens.
