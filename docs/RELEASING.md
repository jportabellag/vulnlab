# Releasing VulnLab

## Pre-release checklist

1. Run repository validation:

```bash
vulnlab verify
```

2. Run Docker-backed checks for changed labs:

```bash
vulnlab verify ssh --docker
vulnlab verify web_ssrf --docker
vulnlab verify multi_host --docker
```

3. Update:

- `CHANGELOG.md`
- `README.md`
- version in `pyproject.toml`

4. Build artifacts:

```bash
python3 -m pip install build
python3 -m build
```

5. Tag and publish:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
