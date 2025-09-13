# shellcheck shell=bash
# Common utilities for setup scripts

set -e          # Exit on command failure.
set -E          # Error traps are inherited.
set -u          # Exit on use of unset variables.
set -o pipefail # Exit if any command in a pipeline fails.

# Function to check required commands
check_required_commands() {
  local commands=("$@")
  for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "ERROR: $cmd command not found"
      echo "Please install it manually according to README.md"
      exit 1
    fi
  done
  echo "All required commands available: ${commands[*]}"
}

# Function to print section headers
print_section() {
  local section_name="$1"
  echo ""
  echo "================================================="
  echo "$section_name"
  echo "================================================="
  echo ""
}
