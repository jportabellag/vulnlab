# Web SSRF Lab Walkthrough

## Goal

Use the fetch feature to reach an internal-only service bound to localhost inside the container.

## Expected path

1. Enumerate:

- `/fetch.php`
- `/debug/`
- `/backup/app.env.bak`

2. Observe the public fetch behavior with a normal external URL.

3. Read `/debug/`, `/assets/connector-readme.txt`, or the backup file to learn that a localhost-only connector still exists.

```text
http://127.0.0.1:9000/
```

4. Use SSRF first to confirm the connector exists, then enumerate paths:

```text
/fetch.php?url=http://127.0.0.1:9000/
/fetch.php?url=http://127.0.0.1:9000/secret
```

5. Extract:

- internal token
- metrics path
- backend-only content

## Learning outcome

- identify SSRF in legitimate backend fetch logic
- pivot to internal services not exposed on the host
