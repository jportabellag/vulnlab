#!/usr/bin/env bash
set -euo pipefail

REPO="${VULNLAB_REPO:-jportabellag/vulnlab}"
VERSION="${1:-latest}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

if [[ "$REPO" == "your-user/vulnlab" ]]; then
  echo "Set VULNLAB_REPO to your real GitHub repo before using this installer." >&2
  echo "Example: VULNLAB_REPO=jportabellag/vulnlab ./install.sh" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin) OS_NAME="darwin" ;;
  Linux) OS_NAME="linux" ;;
  *)
    echo "Unsupported operating system: $(uname -s)" >&2
    exit 1
    ;;
esac

case "$(uname -m)" in
  x86_64|amd64) ARCH_NAME="x86_64" ;;
  arm64|aarch64) ARCH_NAME="arm64" ;;
  *)
    echo "Unsupported architecture: $(uname -m)" >&2
    exit 1
    ;;
esac

ASSET_NAME="vulnlab-${OS_NAME}-${ARCH_NAME}.tar.gz"

if [[ "$VERSION" == "latest" ]]; then
  DOWNLOAD_URL="https://github.com/${REPO}/releases/latest/download/${ASSET_NAME}"
else
  DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${VERSION}/${ASSET_NAME}"
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$INSTALL_DIR"

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

confirm() {
  local prompt="$1"
  local answer
  printf "%s [y/N] " "$prompt"
  read -r answer || true
  case "${answer:-}" in
    y|Y|yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

install_command_for_tool() {
  local tool="$1"
  if command_exists brew; then
    case "$tool" in
      git) echo "brew install git"; return 0 ;;
      docker) echo "brew install --cask docker"; return 0 ;;
      nmap) echo "brew install nmap"; return 0 ;;
    esac
  fi

  if [[ "$OS_NAME" == "linux" ]] && command_exists apt-get; then
    case "$tool" in
      git) echo "apt-get install -y git"; return 0 ;;
      docker) echo "apt-get install -y docker.io"; return 0 ;;
      nmap) echo "apt-get install -y nmap"; return 0 ;;
      redis-cli) echo "apt-get install -y redis-tools"; return 0 ;;
    esac
  fi

  return 1
}

run_install_command() {
  local tool="$1"
  local install_cmd
  if ! install_cmd="$(install_command_for_tool "$tool")"; then
    echo "No automatic installer configured for ${tool} on this system."
    return 1
  fi

  if ! confirm "Install ${tool} using: ${install_cmd}?"; then
    echo "Skipped ${tool} installation."
    return 1
  fi

  if [[ "$EUID" -ne 0 ]] && [[ "$install_cmd" == apt-get* ]]; then
    install_cmd="sudo ${install_cmd}"
  fi

  sh -c "$install_cmd"
}

ensure_path_line() {
  local shell_rc="$1"
  local path_line='export PATH="$HOME/.local/bin:$PATH"'
  touch "$shell_rc"
  if ! grep -Fq "$path_line" "$shell_rc"; then
    printf '\n%s\n' "$path_line" >> "$shell_rc"
    echo "Updated PATH in ${shell_rc}"
  fi
}

bootstrap_dependencies() {
  local required_tools=("git" "docker")
  local optional_tools=("nmap" "redis-cli")
  local tool

  for tool in "${required_tools[@]}"; do
    if ! command_exists "$tool"; then
      echo
      echo "Missing required dependency: ${tool}"
      run_install_command "$tool" || true
    fi
  done

  for tool in "${optional_tools[@]}"; do
    if ! command_exists "$tool"; then
      echo
      echo "Optional tool not found: ${tool}"
      run_install_command "$tool" || true
    fi
  done
}

echo "Downloading ${DOWNLOAD_URL}"

download() {
  if command -v curl >/dev/null 2>&1; then
    if ! curl -fSL "$1" -o "$2"; then
      echo "Download failed: $1" >&2
      echo "Check that the GitHub release exists and includes ${ASSET_NAME}." >&2
      exit 1
    fi
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    if ! wget -O "$2" "$1"; then
      echo "Download failed: $1" >&2
      echo "Check that the GitHub release exists and includes ${ASSET_NAME}." >&2
      exit 1
    fi
    return
  fi

  echo "Neither curl nor wget is installed. Install one of them and retry." >&2
  exit 1
}

download "$DOWNLOAD_URL" "$TMP_DIR/${ASSET_NAME}"
if ! tar -xzf "$TMP_DIR/${ASSET_NAME}" -C "$TMP_DIR"; then
  echo "The downloaded file is not a valid release archive." >&2
  echo "Check that the release asset name matches ${ASSET_NAME}." >&2
  exit 1
fi

if [[ ! -f "$TMP_DIR/vulnlab" ]]; then
  echo "Release archive did not contain the vulnlab binary." >&2
  exit 1
fi

install "$TMP_DIR/vulnlab" "$INSTALL_DIR/vulnlab"

ensure_path_line "$HOME/.bashrc"
ensure_path_line "$HOME/.zshrc"

bootstrap_dependencies

echo
echo "Installed vulnlab to: $INSTALL_DIR/vulnlab"
echo "PATH bootstrap updated for ~/.bashrc and ~/.zshrc."
echo
echo "Next steps:"
echo "  source ~/.bashrc  # or open a new shell"
echo "  vulnlab"
