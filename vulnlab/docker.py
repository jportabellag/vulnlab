from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


class DockerCommandError(RuntimeError):
    pass


def run_docker_command(args: list[str], cwd: Optional[Path] = None, capture_output: bool = False) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=capture_output,
    )

    if result.returncode != 0:
        message = result.stderr.strip() if result.stderr else "Docker command failed"
        raise DockerCommandError(message)

    return result.stdout.strip() if capture_output else ""


def docker_available() -> bool:
    try:
        run_docker_command(["docker", "version"], capture_output=True)
        return True
    except DockerCommandError:
        return False


def build_image(tag: str, context_dir: Path) -> None:
    run_docker_command(["docker", "build", "-t", tag, str(context_dir)])


def run_container(name: str, image: str, ports: list[str]) -> str:
    cmd = ["docker", "run", "-d", "--name", name]
    for port in ports:
        cmd.extend(["-p", port])
    cmd.append(image)
    return run_docker_command(cmd, capture_output=True)


def run_container_advanced(
    name: str,
    image: str,
    ports: list[str] | None = None,
    network: str | None = None,
    aliases: list[str] | None = None,
) -> str:
    cmd = ["docker", "run", "-d", "--name", name]
    for port in ports or []:
        cmd.extend(["-p", port])
    if network:
        cmd.extend(["--network", network])
    for alias in aliases or []:
        cmd.extend(["--network-alias", alias])
    cmd.append(image)
    return run_docker_command(cmd, capture_output=True)


def exec_in_container(name: str, args: list[str]) -> str:
    return run_docker_command(["docker", "exec", name, *args], capture_output=True)


def create_network(name: str) -> None:
    run_docker_command(["docker", "network", "create", name], capture_output=True)


def remove_network(name: str) -> None:
    run_docker_command(["docker", "network", "rm", name], capture_output=True)


def network_exists(name: str) -> bool:
    output = run_docker_command(
        ["docker", "network", "ls", "--filter", f"name=^{name}$", "--format", "{{.Name}}"],
        capture_output=True,
    )
    return name in output.splitlines()


def stop_container(name: str) -> None:
    run_docker_command(["docker", "stop", name], capture_output=True)


def remove_container(name: str, force: bool = False) -> None:
    cmd = ["docker", "rm"]
    if force:
        cmd.append("-f")
    cmd.append(name)
    run_docker_command(cmd, capture_output=True)


def container_exists(name: str) -> bool:
    output = run_docker_command(
        ["docker", "ps", "-a", "--filter", f"name=^{name}$", "--format", "{{.Names}}"],
        capture_output=True,
    )
    return name in output.splitlines()


def container_status(name: str) -> Optional[dict[str, str]]:
    output = run_docker_command(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"name=^{name}$",
            "--format",
            "{{.Names}}|{{.Status}}|{{.Ports}}|{{.Image}}",
        ],
        capture_output=True,
    )

    if not output.strip():
        return None

    parts = output.splitlines()[0].split("|", 3)
    return {
        "name": parts[0],
        "status": parts[1],
        "ports": parts[2],
        "image": parts[3],
    }


def list_vulnlab_containers() -> list[dict[str, str]]:
    output = run_docker_command(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            "name=^vulnlab_",
            "--format",
            "{{.Names}}|{{.Status}}|{{.Ports}}|{{.Image}}",
        ],
        capture_output=True,
    )

    containers = []
    for line in output.splitlines():
        name, status, ports, image = line.split("|", 3)
        containers.append(
            {
                "name": name,
                "status": status,
                "ports": ports,
                "image": image,
            }
        )
    return containers


def container_logs(name: str, tail: int = 50) -> str:
    return run_docker_command(["docker", "logs", "--tail", str(tail), name], capture_output=True)
