# Contributing

## Scope

Contributions should preserve VulnLab's core goals:

- reproducible local labs
- lightweight Docker-based scenarios
- clear educational intent
- intentional, documented vulnerabilities

## Development flow

1. Create or update a lab under `docker/`
2. Register it in `vulnlab/labs.py`
3. Add or update verification checks in `vulnlab/verify.py`
4. Update relevant documentation under `docs/`
5. Run:

```bash
vulnlab verify
vulnlab verify <lab> --docker
```

## Design rules

- Keep labs small and reproducible
- Prefer realistic but readable vulnerable code
- Do not add destructive host-side behavior
- Do not auto-install external tools without confirmation
