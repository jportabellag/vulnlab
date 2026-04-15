# FTP Anonymous Lab Walkthrough

## Goal

Discover anonymous FTP access and recover exposed files.

## Expected path

1. Enumerate:

```bash
nmap -sV -p 2121 localhost
```

2. Connect:

```bash
ftp localhost 2121
```

Use `anonymous` as the username.

3. List directories and retrieve files from:

- `public/`
- `backups/`

4. Inspect:

- `readme.txt`
- `credentials.txt`
- `site-backup.zip`

## Learning outcome

- FTP enumeration
- weak anonymous access discovery
- recovery of exposed legacy material
