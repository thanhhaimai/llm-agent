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
  check_required_commands "brew"

  # Update brew and install required tools
  print_section "Setting up repo for development"
  brew update
  brew install uv direnv

  # If uv.lock exists, sync with locked dependencies; otherwise, sync all packages
  print_section "Syncing dependencies"
  if [ ! -f "../uv.lock" ]; then
    uv sync --all-packages
  else
    uv sync --locked --all-packages
  fi

  # Set up pre-commit hooks
  print_section "Setting up pre-commit hooks"
  uv run pre-commit install

  echo "Setup complete!"

}
