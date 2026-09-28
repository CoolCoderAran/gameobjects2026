
# Contributing to GameObjects

Thank you for your interest in contributing to GameObjects.

GameObjects is a lightweight Python project focused on mathematics, geometry, and utilities for game development. Contributions should prioritize correctness, clarity, maintainability, and a small runtime footprint.

## Before You Begin

Before making a substantial change:

1. Check existing issues and pull requests.
2. Read the relevant documentation.
3. Check whether the proposed feature fits the project's design goals.
4. Open an issue for major API changes or new systems.

Small bug fixes, documentation improvements, and tests may not require an issue beforehand.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/REPLACE_WITH_YOUR_USERNAME/gameobjects.git
cd gameobjects
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Code Standards

Contributions should:

- Use modern Python syntax where supported.
- Include type annotations for public APIs.
- Follow the project's formatting and linting rules.
- Avoid unnecessary runtime dependencies.
- Use clear and descriptive names.
- Preserve mathematical consistency.
- Include tests for new behavior and bug fixes.
- Avoid breaking existing public APIs without discussion.

## Testing

Run the test suite with:

```bash
python -m pytest
```

Run linting with:

```bash
ruff check .
```

Run type checking with:

```bash
mypy src
```

All relevant checks should pass before submitting a pull request.

## Mathematical Changes

Changes involving mathematical behavior should include tests for:

- Normal inputs
- Boundary values
- Zero-length vectors
- Invalid inputs
- Floating-point behavior
- Relevant mathematical identities
- Compatibility with documented API behavior

When appropriate, property-based tests may be used.

## Pull Requests

Pull requests should:

1. Explain what was changed.
2. Explain why the change is needed.
3. Include tests when applicable.
4. Update documentation when the public API changes.
5. Keep unrelated changes out of the pull request.
6. Clearly identify breaking changes.

## Commit Messages

Use concise commit messages that describe the change.

Examples:

```text
Add Vector2 normalization tests
Fix matrix multiplication dimensions
Document zero-length vector behavior
Modernize package metadata
```

## API Stability

The project is currently in an early development stage. Public APIs may change before the first stable release.

Breaking changes should be documented in the changelog.

## Questions

For questions or proposed changes, open an issue in the project repository.
