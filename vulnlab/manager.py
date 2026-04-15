from __future__ import annotations

from vulnlab import docker
from vulnlab.labs import LABS, LabDefinition, ServiceDefinition
from vulnlab.console import animate_progress, print_header, print_info, print_kv, print_success


def _ensure_container_exists(lab: LabDefinition) -> bool:
    if lab.services:
        return any(docker.container_exists(service.container_name) for service in lab.services)
    if lab.container_name and docker.container_exists(lab.container_name):
        return True

    print_info(f"Lab '{lab.slug}' is not currently created.")
    return False


def _build_lab(lab: LabDefinition) -> None:
    if lab.services:
        for service in lab.services:
            docker.build_image(service.image, service.docker_context)
        return

    docker.build_image(lab.image, lab.docker_context)


def _run_lab(lab: LabDefinition) -> None:
    if lab.services:
        if lab.network_name and not docker.network_exists(lab.network_name):
            docker.create_network(lab.network_name)
        for service in lab.services:
            aliases = [service.container_name.replace("vulnlab_", "").replace("_", "-"), service.name, *service.aliases]
            docker.run_container_advanced(
                service.container_name,
                service.image,
                ports=service.ports,
                network=lab.network_name,
                aliases=aliases,
            )
        return

    docker.run_container(lab.container_name, lab.image, lab.ports)


def _remove_lab_runtime(lab: LabDefinition, force: bool = False) -> None:
    if lab.services:
        for service in lab.services:
            if docker.container_exists(service.container_name):
                docker.remove_container(service.container_name, force=force)
        if lab.network_name and docker.network_exists(lab.network_name):
            docker.remove_network(lab.network_name)
        return

    if lab.container_name and docker.container_exists(lab.container_name):
        docker.remove_container(lab.container_name, force=force)


def create_lab(lab: LabDefinition) -> None:
    _remove_lab_runtime(lab, force=True)

    print_header(f"Create Lab: {lab.title}", lab.description)
    animate_progress("Preparing environment", steps=12, delay=0.02)
    _build_lab(lab)
    print_info("Images built")
    _run_lab(lab)
    print_success("Lab created")
    print_kv("Access", lab.access)


def stop_lab(lab: LabDefinition) -> None:
    if not _ensure_container_exists(lab):
        return

    print_header(f"Stop Lab: {lab.title}")
    if lab.services:
        for service in lab.services:
            if docker.container_exists(service.container_name):
                docker.stop_container(service.container_name)
    else:
        docker.stop_container(lab.container_name)
    print_success("Lab stopped")


def remove_lab(lab: LabDefinition) -> None:
    if not _ensure_container_exists(lab):
        return

    print_header(f"Remove Lab: {lab.title}")
    _remove_lab_runtime(lab)
    print_success("Lab removed")


def reset_lab(lab: LabDefinition) -> None:
    print_header(f"Reset Lab: {lab.title}")
    animate_progress("Resetting runtime", steps=12, delay=0.02)
    _remove_lab_runtime(lab, force=True)
    _build_lab(lab)
    _run_lab(lab)
    print_success("Lab reset")
    print_kv("Access", lab.access)


def print_lab_info(lab: LabDefinition) -> None:
    print_header(lab.title, lab.description)
    print_kv("Slug", lab.slug)
    print_kv("Category", lab.category)
    print_kv("Difficulty", lab.difficulty)
    print_kv("Access", lab.access)
    print_kv("Ports", ", ".join(lab.ports))
    print_kv("Tools", ", ".join(lab.tools))
    print("Objectives:")
    for objective in lab.objectives:
        print(f"- {objective}")
    if lab.optional_objectives:
        print("Optional Objectives:")
        for objective in lab.optional_objectives:
            print(f"- {objective}")
    print("Notes:")
    for note in lab.notes:
        print(f"- {note}")


def print_labs() -> None:
    containers = {item["name"]: item for item in docker.list_vulnlab_containers()}

    print_header("Lab Registry", "Available offensive-security training scenarios.")
    for lab in LABS.values():
        if lab.services:
            active = [containers.get(service.container_name) for service in lab.services]
            up_count = sum(1 for item in active if item)
            status = f"{up_count}/{len(lab.services)} services" if up_count else "not created"
            ports = ", ".join(lab.ports)
        else:
            container = containers.get(lab.container_name)
            status = container["status"] if container else "not created"
            ports = container["ports"] if container and container["ports"] else ", ".join(lab.ports)
        print(f"- {lab.slug} | {lab.title} | {lab.difficulty} | {status} | {ports}")


def print_lab_status(lab: LabDefinition) -> None:
    if not _ensure_container_exists(lab):
        return

    if lab.services:
        print_header(f"Lab Status: {lab.title}")
        print_kv("Access", lab.access)
        print_kv("Network", lab.network_name or "n/a")
        for service in lab.services:
            status = docker.container_status(service.container_name)
            if not status:
                continue
            print_kv("Service", service.title)
            print_kv("Container", status["name"])
            print_kv("Image", status["image"])
            print_kv("Status", status["status"])
            print_kv("Ports", status["ports"] or "Private")
        return

    status = docker.container_status(lab.container_name)

    print_header(f"Lab Status: {lab.title}")
    print_kv("Container", status["name"])
    print_kv("Image", status["image"])
    print_kv("Status", status["status"])
    print_kv("Ports", status["ports"] or "Private")
    print_kv("Access", lab.access)


def print_logs(lab: LabDefinition, tail: int = 50) -> None:
    if not _ensure_container_exists(lab):
        return

    print_header(f"Logs: {lab.title}", f"Showing last {tail} lines")
    if lab.services:
        for service in lab.services:
            if docker.container_exists(service.container_name):
                print(f"=== {service.container_name} ===")
                print(docker.container_logs(service.container_name, tail=tail))
        return

    print(docker.container_logs(lab.container_name, tail=tail))
