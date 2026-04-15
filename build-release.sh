#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
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

OS_NAME="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH_NAME="$(uname -m)"
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
