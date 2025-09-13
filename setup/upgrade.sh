#!/usr/bin/env bash

{ # protect against editing while executing

  # Execute in the source dir of the script, regardless where invoked from.
  cd "$(dirname "$0")" || exit

  set -e          # Exit on command failure.
  set -E          # Error traps are inherited.
  set -u          # Exit on use of unset variables.
  set -o pipefail # Exit if any command in a pipeline fails.

  # Source common utilities
  # shellcheck source=/dev/null
  source "setup-utils.sh"

  # Check required commands
  check_required_commands "uv"

  # Change to the project root directory
  cd ".." || exit

  print_section "Verifying Project"

  # Check if we're in a uv project
  if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: pyproject.toml not found. Are you in a uv project directory?"
    exit 1
  fi

  # Check if uv.lock exists
  if [ ! -f "uv.lock" ]; then
    echo "WARNING: uv.lock not found. This will create a new lock file."
  fi

  # Upgrade Python
  print_section "Upgrading Python"
  uv python upgrade

  # Upgrade all dependencies
  print_section "Upgrading Dependencies"
  uv lock --upgrade

  # Upgrade all tools
  print_section "Upgrading Tools"
  uv tool upgrade --all

  # Update pre-commit hooks
  print_section "Updating Pre-commit Hooks"
  uv run pre-commit autoupdate

  # Sync the environment with updated dependencies
  print_section "Syncing Environment"
  uv sync --all-packages

  # Run tests to ensure everything still works
  print_section "Running Tests"
  if uv run pytest; then
    echo "All tests passed"
  else
    echo "Tests failed"
    exit 1
  fi

  echo "Dependency upgrade completed successfully!"

} # protect against editing while executing
