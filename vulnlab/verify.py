from __future__ import annotations

import py_compile
import tempfile
import time
from pathlib import Path

from vulnlab import docker
from vulnlab.labs import BASE_DIR, LABS, LabDefinition


def _python_files() -> list[Path]:
    return [
        BASE_DIR / "main.py",
        BASE_DIR / "vulnlab" / "__init__.py",
        BASE_DIR / "vulnlab" / "cli.py",
        BASE_DIR / "vulnlab" / "console.py",
        BASE_DIR / "vulnlab" / "docs.py",
        BASE_DIR / "vulnlab" / "docker.py",
        BASE_DIR / "vulnlab" / "labs.py",
        BASE_DIR / "vulnlab" / "manager.py",
        BASE_DIR / "vulnlab" / "setup.py",
        BASE_DIR / "vulnlab" / "ui.py",
        BASE_DIR / "vulnlab" / "verify.py",
    ]


def _compile_python() -> list[str]:
    checks = []
    with tempfile.TemporaryDirectory() as tempdir:
        for file_path in _python_files():
            py_compile.compile(str(file_path), cfile=str(Path(tempdir) / f"{file_path.stem}.pyc"), doraise=True)
            checks.append(f"python: {file_path.name}")
    return checks


def _check_structure() -> list[str]:
    checks = []
    required = [
        BASE_DIR / "README.md",
        BASE_DIR / "pyproject.toml",
        BASE_DIR / "docs" / "ROADMAP.md",
    ]

    for lab in LABS.values():
        if lab.services:
            for service in lab.services:
                required.append(service.docker_context / "Dockerfile")
        else:
            required.append(lab.docker_context / "Dockerfile")

    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"Required file is missing: {path}")
        checks.append(f"file: {path.relative_to(BASE_DIR)}")

    return checks


def _verify_lab_runtime(lab: LabDefinition) -> list[str]:
    checks = []

    if lab.services:
        network_name = f"vulnlab_verify_net_{lab.slug}"
        if docker.network_exists(network_name):
            docker.remove_network(network_name)

        for service in lab.services:
            if docker.container_exists(service.container_name):
                docker.remove_container(service.container_name, force=True)

        for service in lab.services:
            docker.build_image(service.image, service.docker_context)
        checks.append(f"docker build: {lab.slug}")

        docker.create_network(network_name)
        try:
            for service in lab.services:
                aliases = [service.name, service.container_name.replace("vulnlab_", "").replace("_", "-"), *service.aliases]
                docker.run_container_advanced(
                    service.container_name,
                    service.image,
                    ports=[],
                    network=network_name,
                    aliases=aliases,
                )
            time.sleep(lab.startup_wait)
            for service in lab.services:
                for command in service.verify_commands:
                    docker.exec_in_container(service.container_name, command)
            checks.append(f"docker runtime: {lab.slug}")
        finally:
            for service in lab.services:
                if docker.container_exists(service.container_name):
                    docker.remove_container(service.container_name, force=True)
            if docker.network_exists(network_name):
                docker.remove_network(network_name)
        return checks

    temp_name = f"vulnlab_verify_{lab.slug}"
    if docker.container_exists(temp_name):
        docker.remove_container(temp_name, force=True)

    docker.build_image(lab.image, lab.docker_context)
    checks.append(f"docker build: {lab.slug}")

    docker.run_container(temp_name, lab.image, [])
    try:
        time.sleep(lab.startup_wait)
        for command in lab.verify_commands:
            docker.exec_in_container(temp_name, command)
        checks.append(f"docker runtime: {lab.slug}")
    finally:
        docker.remove_container(temp_name, force=True)

    return checks


def run_verification(target: str = "all", include_docker: bool = False) -> list[str]:
    checks: list[str] = []
    checks.extend(_compile_python())
    checks.extend(_check_structure())

    if include_docker:
        labs = LABS.values() if target == "all" else [LABS[target]]
        for lab in labs:
            checks.extend(_verify_lab_runtime(lab))

    return checks
