#!/usr/bin/env bash
set -euo pipefail

REPO="${VULNLAB_REPO:-your-user/vulnlab}"
VERSION="${1:-latest}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

case "$(uname -s)" in
  Darwin) OS_NAME="darwin" ;;
  Linux) OS_NAME="linux" ;;
  *)
    echo "Unsupported operating system: $(uname -s)" >&2
    exit 1
    ;;
esac

ARCH_NAME="$(uname -m)"
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
curl -fsSL "$DOWNLOAD_URL" -o "$TMP_DIR/${ASSET_NAME}"
tar -xzf "$TMP_DIR/${ASSET_NAME}" -C "$TMP_DIR"
install "$TMP_DIR/vulnlab" "$INSTALL_DIR/vulnlab"

echo
echo "Installed vulnlab to: $INSTALL_DIR/vulnlab"
echo "Ensure $INSTALL_DIR is in your PATH."
echo
echo "Next steps:"
echo "  vulnlab doctor"
echo "  vulnlab setup"
