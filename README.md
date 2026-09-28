
# GameObjects

A lightweight, dependency-free Python library for game development, mathematics, and geometric operations.

GameObjects is a modern continuation of the historical `gameobjects` project by Will McGugan. The project provides reusable mathematical and utility classes intended to simplify common tasks in game development and interactive applications.

## Features

- Pure Python implementation
- Zero third-party runtime dependencies
- Lightweight and fast to install
- Modern Python type annotations
- Vector and matrix mathematics
- Geometry utilities
- Sequence-compatible mathematical objects
- Designed for use in games, simulations, and interactive applications
- Open development and testing workflow

Additional features will be documented as they become available.

## Installation

Install the latest published version using pip:

```bash
python -m pip install gameobjects
```

For development installations, clone the repository and install it locally:

```bash
git clone https://github.com/REPLACE_WITH_YOUR_USERNAME/gameobjects.git
cd gameobjects
python -m pip install -e ".[dev]"
```

## Quick Example

```python
from gameobjects.vector2 import Vector2

position = Vector2(10, 20)
velocity = Vector2(2, 3)

new_position = position + velocity

print(new_position)
```

> The API shown above will be finalized during the modernization process.

## Project Status

GameObjects is currently being modernized from the historical 0.0.3 codebase.

The modernization process includes:

- Updating the codebase for modern Python
- Improving type annotations
- Adding automated tests
- Preserving useful historical behavior where practical
- Improving mathematical consistency and safety
- Expanding the documentation
- Publishing modern Python packages

The API may change before the first stable release.

## Design Goals

The project aims to remain:

- **Small:** Avoid unnecessary framework-level complexity.
- **Fast to install:** Provide lightweight wheels and no runtime dependencies.
- **Portable:** Work across supported operating systems.
- **Readable:** Use clear and maintainable Python.
- **Reliable:** Test mathematical behavior and edge cases.
- **Extensible:** Allow additional mathematical and game-development features without making the core unnecessarily large.

## Runtime Dependencies

GameObjects is designed to have no third-party runtime dependencies.

Development tools, such as testing and linting packages, may be installed separately.

## Documentation

Documentation will be expanded as the modernized API is implemented.

Planned documentation includes:

- Vector classes
- Matrix classes
- Geometry utilities
- Transformations
- Numerical behavior
- API reference
- Examples and tutorials

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

## License

The historical project metadata identified GameObjects as public domain. The applicable licensing status and provenance of the original source must be verified before the final license is selected for the modernized project.

See [LICENSE](LICENSE) for the current licensing notice.

## Acknowledgments

This project is based on the historical GameObjects project originally created by Will McGugan.

The modernized project is intended to preserve useful ideas from the original codebase while providing a maintained, tested, and modern Python implementation.
