# Roadmap

## Current State

- Modular CLI under `vulnlab/`
- Central lab registry
- Reusable Docker runtime layer
- Interactive terminal menu
- Guided dependency checks and setup flow
- Verification support for repository checks and Docker-backed runtime checks

## Current Lab Coverage

- `ssh`
- `web`
- `web_upload`
- `web_cmdi`
- `web_ssrf`
- `web_traversal`
- `redis_misconfig`
- `ftp_anon`
- `multi_host`

## Next Recommended Areas

### Platform

- configurable host ports via CLI flags
- JSON output mode for automation
- GitHub Actions CI for `verify`
- release automation for tagged versions

### Labs

- `web_deserialization`
- `path_confusion` or archive extraction abuse

### Learning Content

- optional hints per lab
- blue-team remediation notes
- screenshots and terminal demos for the README
- guided progression tracks by difficulty

## Quality Bar For New Labs

- reproducible startup
- clear vulnerable surface
- realistic but readable implementation
- resettable runtime state
- documented goals, tools, and walkthrough
