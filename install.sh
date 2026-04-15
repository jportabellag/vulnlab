#!/usr/bin/env bash
set -euo pipefail

REPO="${VULNLAB_REPO:-jportabellag/vulnlab}"
VERSION="${1:-latest}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

if [[ "$REPO" == "jportabellag/vulnlab" ]]; then
  echo "Set VULNLAB_REPO to your real GitHub repo before using this installer." >&2
  echo "Example: VULNLAB_REPO=jordiportabella/vulnlab ./install.sh" >&2
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

echo "Downloading ${DOWNLOAD_URL}"

download() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$1" -o "$2"
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -qO "$2" "$1"
    return
  fi

  echo "Neither curl nor wget is installed. Install one of them and retry." >&2
  exit 1
}

download "$DOWNLOAD_URL" "$TMP_DIR/${ASSET_NAME}"
tar -xzf "$TMP_DIR/${ASSET_NAME}" -C "$TMP_DIR"
install "$TMP_DIR/vulnlab" "$INSTALL_DIR/vulnlab"

echo
echo "Installed vulnlab to: $INSTALL_DIR/vulnlab"
echo "Ensure $INSTALL_DIR is in your PATH."
echo
echo "Next steps:"
echo "  vulnlab doctor"
echo "  vulnlab setup"
