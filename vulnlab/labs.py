from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from vulnlab.paths import get_asset_root


BASE_DIR = get_asset_root()


@dataclass(frozen=True)
class ServiceDefinition:
    name: str
    title: str
    docker_context: Path
    image: str
    container_name: str
    ports: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    verify_commands: list[list[str]] = field(default_factory=list)


@dataclass(frozen=True)
class LabDefinition:
    slug: str
    title: str
    description: str
    category: str
    difficulty: str
    docker_context: Path | None
    image: str | None
    container_name: str | None
    ports: list[str]
    access: str
    tools: list[str]
    objectives: list[str]
    optional_objectives: list[str]
    notes: list[str]
    verify_commands: list[list[str]]
    startup_wait: int = 2
    services: list[ServiceDefinition] = field(default_factory=list)
    network_name: str | None = None


LABS: dict[str, LabDefinition] = {
    "ssh": LabDefinition(
        slug="ssh",
        title="SSH Weak Access Lab",
        description="SSH server with a weak foothold, credential recovery, and a less obvious privilege-escalation path.",
        category="network",
        difficulty="medium-hard",
        docker_context=BASE_DIR / "docker" / "ssh_vuln",
        image="vulnlab-ssh",
        container_name="vulnlab_ssh",
        ports=["2222:22"],
        access="ssh user@localhost -p 2222",
        tools=["nmap", "ssh", "hydra"],
        objectives=[
            "Enumerate the exposed SSH service",
            "Gain initial access with a weak foothold account",
            "Recover a second account through local archive enumeration",
            "Escalate through a less obvious privileged backup path",
        ],
        optional_objectives=[
            "Foothold: gain shell access with a weak account",
            "Data access: recover credential material from a legacy archive export",
            "Privilege escalation: identify and abuse the report backup path",
        ],
        notes=[
            "Only the initial foothold is directly weak",
            "Root SSH login is disabled",
            "Post-access escalation depends on enumeration rather than a single obvious artifact",
        ],
        verify_commands=[
            ["sh", "-lc", "sshd -t"],
            ["sh", "-lc", "getent passwd user && getent passwd analyst"],
            ["sh", "-lc", "[ -f /srv/backups/helpdesk-export.tgz ] && [ -x /usr/local/bin/backup_reports.sh ]"],
            ["sh", "-lc", "sudo -l -U analyst | grep -q '/usr/local/bin/backup_reports.sh'"],
        ],
        startup_wait=2,
    ),
    "web": LabDefinition(
        slug="web",
        title="Web SQLi Lab",
        description="Vulnerable PHP application with SQLi login, hidden routes, and exposed backups.",
        category="web",
        difficulty="easy-medium",
        docker_context=BASE_DIR / "docker" / "web_vuln",
        image="vulnlab-web",
        container_name="vulnlab_web",
        ports=["8080:80"],
        access="http://localhost:8080",
        tools=["nmap", "ffuf", "dirsearch", "browser", "sqlmap"],
        objectives=[
            "Enumerate web attack surface and hidden routes",
            "Detect SQL injection in login and search flows",
            "Recover internal data through a second-step action after foothold",
        ],
        optional_objectives=[
            "Foothold: gain authenticated access through SQL injection",
            "Data access: recover hidden files or API data after foothold",
        ],
        notes=[
            "Hidden routes still exist but are less directly hinted",
            "Some endpoints are noisy or decoy content",
        ],
        verify_commands=[
            ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'Intranet Portal') !== false ? 0 : 1);"],
            ["sh", "-lc", "[ -f /var/www/html/backup/config.php.bak ]"],
        ],
        startup_wait=3,
    ),
    "web_upload": LabDefinition(
        slug="web_upload",
        title="Web Upload And LFI Lab",
        description="PHP application with insecure file upload, local file inclusion, and exposed dev routes.",
        category="web",
        difficulty="medium",
        docker_context=BASE_DIR / "docker" / "web_upload_vuln",
        image="vulnlab-web-upload",
        container_name="vulnlab_web_upload",
        ports=["8081:80"],
        access="http://localhost:8081",
        tools=["nmap", "ffuf", "dirsearch", "browser", "burpsuite"],
        objectives=[
            "Discover hidden development routes",
            "Abuse an insecure file upload flow",
            "Chain upload and local file inclusion in two steps",
        ],
        optional_objectives=[
            "Foothold: upload a file that can influence server-side include behavior",
            "Data access: include uploaded content or local files through the viewer",
        ],
        notes=[
            "Uploading a file is not enough on its own",
            "The viewer becomes useful only after you identify a second step",
        ],
        verify_commands=[
            ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'Upload Center') !== false ? 0 : 1);"],
            ["sh", "-lc", "[ -d /var/www/html/uploads ] && [ -f /var/www/html/backup/dev-config.php.bak ]"],
        ],
        startup_wait=3,
    ),
    "web_cmdi": LabDefinition(
        slug="web_cmdi",
        title="Web Command Injection Lab",
        description="PHP application with a diagnostics feature vulnerable to command injection and exposed internal files.",
        category="web",
        difficulty="medium",
        docker_context=BASE_DIR / "docker" / "web_cmdi_vuln",
        image="vulnlab-web-cmdi",
        container_name="vulnlab_web_cmdi",
        ports=["8082:80"],
        access="http://localhost:8082",
        tools=["nmap", "ffuf", "dirsearch", "browser", "burpsuite"],
        objectives=[
            "Detect a parameter vulnerable to command injection",
            "Bypass weak input filtering",
            "Extract local information from the web server",
        ],
        optional_objectives=[
            "Foothold: achieve command execution despite weak filters",
            "Data access: read exported configuration or local files",
        ],
        notes=[
            "The diagnostics page applies weak blacklist filtering",
            "Some internal pages are decoys and some contain useful context",
        ],
        verify_commands=[
            ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'NetOps Console') !== false ? 0 : 1);"],
            ["sh", "-lc", "[ -f /var/www/html/exports/netops-config.bak ]"],
        ],
        startup_wait=3,
    ),
    "web_ssrf": LabDefinition(
        slug="web_ssrf",
        title="Web SSRF Lab",
        description="PHP application with an SSRF-prone fetcher and an internal service reachable only from localhost.",
        category="web",
        difficulty="medium-hard",
        docker_context=BASE_DIR / "docker" / "web_ssrf_vuln",
        image="vulnlab-web-ssrf",
        container_name="vulnlab_web_ssrf",
        ports=["8083:80"],
        access="http://localhost:8083",
        tools=["nmap", "ffuf", "browser", "burpsuite", "curl"],
        objectives=[
            "Identify a feature that fetches remote URLs",
            "Discover an internal service exposed only on localhost",
            "Use SSRF to access content not reachable externally",
        ],
        optional_objectives=[
            "Foothold: identify a fetch primitive that the backend will execute",
            "Data access: recover internal-only material through SSRF",
        ],
        notes=[
            "The internal backend still exists but clues are less direct",
            "Some files and routes are noisy and not all of them matter",
        ],
        verify_commands=[
            ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'Remote Fetch Console') !== false ? 0 : 1);"],
            ["python3", "-c", "import urllib.request; data=urllib.request.urlopen('http://127.0.0.1:9000/secret').read().decode(); raise SystemExit(0 if 'INTERNAL_TOKEN' in data else 1)"],
        ],
        startup_wait=4,
    ),
    "ftp_anon": LabDefinition(
        slug="ftp_anon",
        title="FTP Anonymous Lab",
        description="FTP server with anonymous access and exposed backup files for service-enumeration practice.",
        category="network",
        difficulty="easy-medium",
        docker_context=BASE_DIR / "docker" / "ftp_anon_vuln",
        image="vulnlab-ftp-anon",
        container_name="vulnlab_ftp_anon",
        ports=["2121:21"],
        access="ftp localhost 2121",
        tools=["nmap", "ftp", "hydra"],
        objectives=[
            "Detect an accessible FTP service",
            "Confirm anonymous access and enumerate exposed content",
            "Locate backups and legacy credentials on the service",
        ],
        optional_objectives=[
            "Foothold: authenticate through anonymous access",
            "Data access: recover files from the exposed backup tree",
        ],
        notes=[
            "Anonymous login is enabled",
            "Public directories and backups are accessible over FTP",
        ],
        verify_commands=[
            ["sh", "-lc", "ps aux | grep '[v]sftpd' >/dev/null"],
            ["sh", "-lc", "[ -f /srv/ftp/public/readme.txt ] && [ -f /srv/ftp/backups/site-backup.zip ]"],
        ],
        startup_wait=3,
    ),
    "redis_misconfig": LabDefinition(
        slug="redis_misconfig",
        title="Redis Misconfiguration Lab",
        description="Exposed Redis service without authentication, noisy data, and recoverable operational secrets.",
        category="network",
        difficulty="medium-hard",
        docker_context=BASE_DIR / "docker" / "redis_misconfig_vuln",
        image="vulnlab-redis-misconfig",
        container_name="vulnlab_redis_misconfig",
        ports=["6380:6379"],
        access="redis-cli -h localhost -p 6380",
        tools=["nmap", "redis-cli", "netcat"],
        objectives=[
            "Identify an exposed Redis service with weak configuration",
            "Enumerate keys and runtime settings without authentication",
            "Recover sensitive operational material from stored data",
        ],
        optional_objectives=[
            "Foothold: confirm unauthenticated Redis access",
            "Data access: recover the sync credentials and snapshot hints",
            "Impact: identify what an attacker could change or persist through Redis",
        ],
        notes=[
            "Protected mode is disabled and no password is configured",
            "Several keys are noise; not every value is useful",
        ],
        verify_commands=[
            ["redis-cli", "PING"],
            ["sh", "-lc", "redis-cli GET public:welcome | grep -q 'Cache node ready'"],
            ["sh", "-lc", "redis-cli HGETALL ops:sync | grep -q 'sync-redis-2024'"],
        ],
        startup_wait=3,
    ),
    "web_traversal": LabDefinition(
        slug="web_traversal",
        title="Web Traversal And Token Reuse Lab",
        description="PHP document portal with naive traversal filtering, token reuse, and staged internal data access.",
        category="web",
        difficulty="hard",
        docker_context=BASE_DIR / "docker" / "web_traversal_vuln",
        image="vulnlab-web-traversal",
        container_name="vulnlab_web_traversal",
        ports=["8085:80"],
        access="http://localhost:8085",
        tools=["nmap", "ffuf", "dirsearch", "browser", "burpsuite", "curl"],
        objectives=[
            "Enumerate a document portal and its legacy download flow",
            "Bypass naive traversal filtering to read files outside the web root",
            "Use recovered internal material to perform a second-stage data access action",
        ],
        optional_objectives=[
            "Foothold: identify the vulnerable download primitive",
            "Data access: recover the internal export token through traversal",
            "Pivot: use the recovered token to access protected export data",
        ],
        notes=[
            "The portal contains decoy files and normal downloads",
            "Reading a file is not the end state; a second action is required",
        ],
        verify_commands=[
            ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'Document Gateway') !== false ? 0 : 1);"],
            ["php", "-r", "$data=file_get_contents('http://127.0.0.1/download.php?file=....//....//....//opt/vulnlab/config/portal.env'); exit(strpos($data, 'EXPORT_TOKEN=export-token-7421') !== false ? 0 : 1);"],
            ["php", "-r", "$ctx=stream_context_create(['http' => ['header' => \"X-Lab-Token: export-token-7421\\r\\n\"]]); $data=file_get_contents('http://127.0.0.1/admin/export.php', false, $ctx); exit(strpos($data, 'INTERNAL_EXPORT_OK') !== false ? 0 : 1);"],
        ],
        startup_wait=3,
    ),
}

LABS["multi_host"] = LabDefinition(
    slug="multi_host",
    title="Multi Host Pivot Lab",
    description="Scenario with a vulnerable web gateway and an internal service reachable only from the lab Docker network.",
    category="multi-host",
    difficulty="hard",
    docker_context=None,
    image=None,
    container_name=None,
    ports=["8084:80"],
    access="http://localhost:8084",
    tools=["nmap", "ffuf", "browser", "burpsuite", "curl"],
    objectives=[
        "Compromise a gateway exposed to the host machine",
        "Discover an internal host that is not published locally",
        "Move laterally to an internal service through the compromised gateway",
    ],
    optional_objectives=[
        "Foothold: gain control of the gateway request primitive",
        "Pivot: reach the internal panel through the gateway",
        "Data access: recover internal-only secrets from the private service",
    ],
    notes=[
        "The internal service does not publish ports to the host machine",
        "The private host alias is less obvious and the useful data requires a second relay step",
    ],
    verify_commands=[],
    startup_wait=4,
    network_name="vulnlab_pivot_net",
    services=[
        ServiceDefinition(
            name="gateway",
            title="Vulnerable gateway",
            docker_context=BASE_DIR / "docker" / "multi_host_gateway",
            image="vulnlab-multi-gateway",
            container_name="vulnlab_multi_gateway",
            ports=["8084:80"],
            aliases=["edge-gateway"],
            verify_commands=[
                ["php", "-r", "exit(strpos(file_get_contents('http://127.0.0.1/'),'Pivot Gateway') !== false ? 0 : 1);"],
                ["sh", "-lc", "getent hosts ops-relay-cache >/dev/null"],
            ],
        ),
        ServiceDefinition(
            name="internal",
            title="Internal panel",
            docker_context=BASE_DIR / "docker" / "multi_host_internal",
            image="vulnlab-multi-internal",
            container_name="vulnlab_multi_internal",
            ports=[],
            aliases=["ops-relay-cache"],
            verify_commands=[
                ["python3", "-c", "import urllib.request; data=urllib.request.urlopen('http://127.0.0.1:8080/').read().decode(); raise SystemExit(0 if 'Internal Admin Panel' in data else 1)"],
                ["python3", "-c", "import urllib.request; req=urllib.request.Request('http://127.0.0.1:8080/relay/secret', headers={'X-Relay-Key': 'relay-stage-two'}); data=urllib.request.urlopen(req).read().decode(); raise SystemExit(0 if 'INTERNAL_DB_USER' in data else 1)"],
            ],
        ),
    ],
)


def get_lab(slug: str) -> LabDefinition | None:
    return LABS.get(slug)
