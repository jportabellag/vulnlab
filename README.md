# VulnLab

VulnLab is a terminal-first toolkit for spinning up intentionally vulnerable local labs with Docker.
It is designed for ethical hacking practice, security training, demos, and classroom use without relying on heavyweight virtual machines or external lab platforms.

## Features

- Terminal-first UX with an interactive hacker-style menu
- One-command lab lifecycle management
- Multiple vulnerability classes across web, network, and pivoting scenarios
- Docker-backed reproducibility
- Built-in verification for Python structure and Docker runtime checks
- Setup and doctor commands for environment readiness

## Lab Catalog

| Slug | Category | Focus |
| --- | --- | --- |
| `ssh` | Network | Weak SSH foothold, credential recovery, tar wildcard privilege escalation |
| `web` | Web | SQL injection, hidden routes, exposed backups |
| `web_upload` | Web | Unrestricted file upload, LFI |
| `web_cmdi` | Web | Command injection |
| `web_ssrf` | Web | SSRF against an internal-only service |
| `web_traversal` | Web | Path traversal, filter bypass, token reuse |
| `redis_misconfig` | Network | Exposed Redis, no auth, secret recovery |
| `ftp_anon` | Network | Anonymous FTP with exposed files |
| `multi_host` | Multi-host | Gateway compromise, relay abuse, and two-step lateral movement |

## Installation

`git clone` on its own does not install the `vulnlab` command into your shell. For end users, the intended installation path should be a prebuilt release binary.

### Recommended: release binary install

```bash
curl -fsSL https://raw.githubusercontent.com/your-user/vulnlab/main/install.sh | bash
```

This installs a standalone `vulnlab` binary into `~/.local/bin` by default, so end users do not need to install Python separately.
The installer also offers to install core system dependencies and updates shell PATH entries for common shells.

### Python-based install for development

```bash
pipx install git+https://github.com/your-user/vulnlab.git
```

### Editable development install

```bash
git clone https://github.com/your-user/vulnlab.git
cd vulnlab
python3 -m pip install -e .
```

After installation:

```bash
source ~/.bashrc  # or open a new shell
vulnlab
```

## Requirements

- Docker
- Git

For source installs and development:

- Python 3.9+

`vulnlab setup` and first launch can optionally attempt installation of missing external tools and will always ask for confirmation first.

## Quick Start

Interactive mode:

```bash
vulnlab
```

Command mode:

```bash
vulnlab list
vulnlab info web
vulnlab create web
vulnlab status web
vulnlab logs web --tail 100
vulnlab reset web
vulnlab remove web
```

## CLI Commands

- `vulnlab`: launch the interactive terminal UI
- `vulnlab menu`: explicit interactive mode
- `vulnlab list`: list all available labs and runtime status
- `vulnlab info <lab>`: show lab metadata, tooling, objectives, and notes
- `vulnlab create <lab>`: build and start a lab
- `vulnlab status <lab>`: inspect running status
- `vulnlab logs <lab> --tail N`: fetch container logs
- `vulnlab stop <lab>`: stop a lab
- `vulnlab reset <lab>`: rebuild and recreate a lab
- `vulnlab remove <lab>`: remove lab runtime artifacts
- `vulnlab doctor`: inspect required external tooling
- `vulnlab setup`: guided setup with confirmation prompts for external installs
- `vulnlab verify`: validate Python files and repository structure
- `vulnlab verify <lab> --docker`: validate build and runtime behavior of a lab

## Verification

Fast repository checks:

```bash
vulnlab verify
```

Runtime verification examples:

```bash
vulnlab verify ssh --docker
vulnlab verify web_ssrf --docker
vulnlab verify web_traversal --docker
vulnlab verify redis_misconfig --docker
vulnlab verify multi_host --docker
```

## Walkthroughs

Each lab has a written walkthrough under `docs/solutions/`, and the CLI can print them directly:

```bash
vulnlab walkthrough web
vulnlab walkthrough multi_host
```

Use walkthroughs as validation material, workshop content, or internal trainer notes.

## Is It Publishable?

Yes, as an open source training project it is now publishable if you position it correctly.

What it already does well:

- provides a consistent terminal UX
- ships multiple vulnerability classes
- supports reproducible local execution
- includes built-in verification
- includes per-lab walkthrough material

What it still is not:

- a full replacement for large hosted offensive-security platforms
- a deep enterprise simulation framework
- a mature CI/release pipeline yet

The right framing is:

- local Docker-based security training labs
- lightweight offensive-security practice kit
- education, workshops, demos, and self-study

## Project Structure

```text
vulnlab/
  cli.py
  console.py
  docker.py
  labs.py
  manager.py
  setup.py
  ui.py
  verify.py

docker/
  ssh_vuln/
  web_vuln/
  web_upload_vuln/
  web_cmdi_vuln/
  web_ssrf_vuln/
  web_traversal_vuln/
  redis_misconfig_vuln/
  ftp_anon_vuln/
  multi_host_gateway/
  multi_host_internal/
```

## Release Workflow

```bash
vulnlab verify
vulnlab verify multi_host --docker
python3 -m pip install -e .[build]
bash build-release.sh
```

See [docs/RELEASING.md](docs/RELEASING.md) for a structured release checklist.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
