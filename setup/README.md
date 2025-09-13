# Setup Scripts

This directory contains setup and maintenance scripts for the llm-agent project.
These scripts automate the development environment setup and maintenance tasks.

## Scripts Overview

- **`setup.sh`**: Initial development environment setup
- **`upgrade.sh`**: Comprehensive environment upgrade and maintenance
- **`setup-utils.sh`**: Utility library used by other scripts

## `setup.sh` - Initial Setup

The initial setup script that prepares your development environment for the first time.

The script is designed to be **idempotent** - you can safely re-run it multiple times without issues.

### What it does

- **Installs required tools**: Uses Homebrew to install `uv` (Python package manager) and `direnv` (environment management)
- **Sets up dependencies**: Syncs project dependencies using `uv sync` (creates lock file if none exists)
- **Configures pre-commit**: Installs pre-commit hooks for automated code quality checks
- **Environment preparation**: Ensures your development environment is ready for the project

### Prerequisites

- **macOS or Linux** with Homebrew support
- **Homebrew** installed (`brew` command available)
  - Install from: <https://brew.sh/>

### Usage

```bash
./setup/setup.sh
```

## `upgrade.sh` - Comprehensive Upgrade

Comprehensive upgrade script that upgrades Python, dependencies, tools, and runs the full test suite.

### What gets upgraded

- **Python**: Latest Python version via `uv python upgrade`
- **Dependencies**: All project dependencies via `uv lock --upgrade`
- **Tools**: All development tools via `uv tool upgrade --all`
- **Pre-commit hooks**: Updates pre-commit hooks to their latest versions via `pre-commit autoupdate`
- **Environment**: Virtual environment synchronization

### Prerequisites

- `setup/setup.sh` has been run successfully
- A valid `pyproject.toml` file in the project root
- Existing `uv.lock` file (created by initial setup)

### Usage

```bash
./setup/upgrade.sh
```

## Best Practices

### For scripts

- Have `{ }` to guard against editing while executing.
- Set `set -eEuo pipefail`. See the current script for comments.
- Source `setup-utils.sh`
- Check for any required command at the start of the script.
- Work for both Mac / Ubuntu.

See `setup.sh` for example

### For Shell libraries

- Has no execution permission
- Has `# shellcheck shell=bash` at the start
- Set `set -eEuo pipefail`. See the current script for comments.
- Prefer `local` variable

See `setup-utils.sh` for example

## Troubleshooting

### Setup Script Issues

#### Script fails with "brew command not found"

- Install Homebrew first: <https://brew.sh/>

### Upgrade Script Issues

#### Script fails with "uv command not found"

**Solution**: Ensure `setup/setup.sh` has been run successfully

```bash
./setup/setup.sh
```

### General Issues

#### Tests fail after upgrade

This indicates a compatibility issue. Consider:

1. **Rollback**: Restore the previous `uv.lock` file
1. **Incremental upgrade**: Upgrade packages one by one to identify the problematic package
1. **Check changelog**: Review the package's changelog for breaking changes
1. **Review test output**: Check specific failure details in test output
1. **Update tests**: Your tests may need updates for new package versions

#### Tool upgrade fails

**Solution**: Some tools may require manual intervention

1. Check tool-specific documentation for upgrade requirements
1. Consider upgrading tools individually if needed
1. Verify tool compatibility with your Python version
1. Check for tool-specific configuration requirements

#### Lock file conflicts

**Solution**: Regenerate the lock file

```bash
uv lock --upgrade
```

#### Environment inconsistencies

**Solution**: Synchronize your environment

```bash
uv sync --all-packages
```

#### Python version issues

**Solution**: Check Python version and upgrade if needed

```bash
uv python list
uv python upgrade
```

### Performance Issues

#### Slow dependency resolution

**Solution**: Use uv's caching features

```bash
uv cache clean  # Clear cache if corrupted
```

#### Large lock file

**Solution**: Review and optimize dependencies

```bash
uv tree  # View dependency tree
```
