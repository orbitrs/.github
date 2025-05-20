# Orbit UI Framework Ecosystem

This repository contains the Orbit UI framework ecosystem - a Rust-first, cross-platform UI framework for building Web, Native, and Embedded applications.

## Project Structure

The Orbit ecosystem consists of the following components:

- **[orbit](./orbit)**: The core Orbit UI framework - provides the rendering engine, component model, and framework APIs
- **[orbit-analyzer](./orbit-analyzer)**: Static analysis tool for `.orbit` files - ensures code quality and best practices
- **[orbitkit](./orbitkit)**: Pre-built component library with UI elements and utilities
- **[orbiton](./orbiton)**: CLI tooling for project management, development, and deployment

## Getting Started

```bash
# Install the CLI tool
cargo install orbiton

# Create a new Orbit project
orbiton new my-app
cd my-app

# Start development server
orbiton dev
```

## Development Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/orbitrs/orbit.git
   cd orbit
   ```

2. Build all projects:
   ```bash
   cargo build --workspace
   ```

3. Run tests:
   ```bash
   cargo test --workspace
   ```

## Documentation

- Main documentation is available in each project's README.md
- Architecture and design specifications can be found in the [docs](./docs) directory
- For component syntax and semantics, refer to [orbit-spec.md](./orbit/orbit-spec.md)
- View our development roadmap and milestones in the [roadmap](./docs/roadmap) directory

## Contributing

Please see our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to contribute to the Orbit ecosystem.

## License

This project is licensed under either:

- [MIT License](./LICENSE-MIT)
- [Apache License, Version 2.0](./LICENSE-APACHE)

at your option.
