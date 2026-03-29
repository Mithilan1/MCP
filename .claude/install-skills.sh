#!/usr/bin/env bash
# Copy the project-scoped Claude skills into ~/.claude/skills on macOS/Linux.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills"
TARGET_DIR="$HOME/.claude/skills"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Expected project skills at $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"
echo "Copying HabitFlow Claude skills to $TARGET_DIR..."

for skill_dir in "$SOURCE_DIR"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$TARGET_DIR/$skill_name"
  cp -R "$skill_dir" "$TARGET_DIR/$skill_name"
  echo "Installed $skill_name"
done

echo ""
echo "Claude user skills now mirror the project's .claude/skills folder."
