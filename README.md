# AndrusOne-FieldOps

Practical tools for real-world engineering—quiet, reliable, and battle-tested.

## What Is This?

AndrusOne-FieldOps is a curated collection of production-ready scripts and utilities drawn directly from real-world projects. These tools are designed for engineers and practitioners who value clarity, dependability, and quiet results over flash.

If DevKit sets up your environment, FieldOps helps you get the job done.

## Why FieldOps?

In the field, the only scripts that matter are the ones that work. This repo focuses on:

- Proven tools that solve recurring problems
- Simple interfaces, well-structured logic, and quiet operation
- Design for reliability and ease of extension
- Field-tested routines that reduce risk and increase speed

Every script in this kit has been used to solve a real problem—and it's documented so you can do the same.

## Quick Start

Clone the repository:

```bash
git clone git@github.com:your-user/andrusone-fieldops.git
cd andrusone-fieldops
```

Run or inspect the included scripts, or copy patterns for your own use.

Some tools have environment verification steps or configuration helpers:

```bash
./scripts/devkit-prereqs.sh            # Installs required packages for Python, Git, and pre-commit
./scripts/devkit-poetry-setup.sh       # Installs Poetry and configures it for isolated environments
./scripts/devkit-ssh-setup.sh          # Configures Git SSH signing and verifies SSH auth
./scripts/devkit-verify-env.sh         # Checks your system for required tools and versions
./scripts/devkit-verify-precommit.sh   # Ensures pre-commit hooks are installed and functional
```

## What You Get Out of the Box

- Python: Clean, dependable scripts with optional Poetry support
- Shell: Bash utilities for system automation
- PowerShell: Cross-platform support for Windows ops and task scripting
- SQL: Analysis helpers and validation queries across dialects
- Git: Structured repo with clean commit hygiene and pre-commit support
- Scripts: Consistent layout, clear docstrings, and quiet output by default

## Project Layout

```text
andrusone-fieldops/
│
├── python/                    # Python tools and scripts
├── shell/                     # Shell scripts by OS flavor
│   ├── ubuntu/
│   ├── rhel/
│   └── centos/
├── powershell/                # PowerShell scripts for cross-platform ops
├── sql/                       # SQL diagnostics, analysis, or migration helpers
│   ├── tsql/
│   ├── ansi/
│   ├── snowflake/
│   ├── plsql/
│   └── source/
├── .pre-commit-config.yaml    # Optional pre-commit config for formatting/linting
├── pyproject.toml             # Python tool configuration
├── requirements.txt           # Python dependencies (if not using Poetry)
├── README.md                  # You're reading it
└── .editorconfig              # Shared formatting rules for text editors
```

## Field Notes and Documentation

Each script is featured on [andrusone.dev](https://andrusone.dev), where it’s explained in plain language for:

- Engineers: Technical usage, input/output behavior, and extension ideas
- Business Leaders: How it reduces risk, saves time, or improves accuracy
- End Users: What it enables and how to benefit from it

## Contributing

Got something to add? Want to improve clarity or reuse?

1. Fork the repo
2. Create a feature branch
3. Submit a pull request with a clear explanation of value and usage

## Philosophy

These tools are designed with care and used with confidence.

FieldOps isn't about clever scripts—it's about tools that work when it matters.
