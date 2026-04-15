#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR="$ROOT_DIR/build"

cd "$ROOT_DIR"

rm -rf "$BUILD_DIR" "$DIST_DIR/vulnlab"

python3 -m PyInstaller \
  --name vulnlab \
  --onefile \
  --clean \
  --paths "$ROOT_DIR" \
  main.py

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

PACKAGE_DIR="$DIST_DIR/release"
PACKAGE_NAME="vulnlab-${OS_NAME}-${ARCH_NAME}"

rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"
cp "$DIST_DIR/vulnlab" "$PACKAGE_DIR/vulnlab"
cp README.md LICENSE "$PACKAGE_DIR/"

tar -C "$PACKAGE_DIR" -czf "$DIST_DIR/${PACKAGE_NAME}.tar.gz" .

echo "Built:"
echo "  $DIST_DIR/vulnlab"
echo "  $DIST_DIR/${PACKAGE_NAME}.tar.gz"
