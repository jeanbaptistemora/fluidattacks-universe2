# Architectural Decision Record

## 2020-12-20 - Why rewriting the whole build system

- Writing a pure build system is painful for 1 developer, 1 time
- Using a pure build system is delicious for all developers, all times thereafter
- See: https://gitlab.com/fluidattacks/product/-/issues/3836, for details

## 2020-12-21 - Why ./m instead of `nix flake`

- Procedures can be executed at 1 command of distance, easy to remember
- Teaching ./m to people is teaching:
  - How to install nix
  - How to type ./m in the console
- Teaching flakes to people in non-NixOS systems is teaching:
  - How to install nix
  - How to set the nix.conf with needed configuration values
  - How to use the new CLI
  - How to use nix-shell with a long -I nixpkgs=hash
  - How to build/run apps and packages from the flake
- ./m uses flakes under the hood, but hides/automatize the complexity
- Additionally a default.nix is added for compatibility reasons,
  so people can nix-env us

## 2020-12-22 - Flakes's packages versus Flakes's apps

- Understand `build` as a mathematical function (`pkgs.stdenv.mkDerivation`)
- A build has inputs and outputs
- A build is deterministic
- Deterministic means that the result only depends on the
  inputs declared in the Nix derivation
  and building something with the same inputs always produce
  the same (cryptographic) outputs
- When you build something, the build is deterministic
- When you build an app, the build is deterministic, too
- When you run the app, the output may or may not be deterministic
- We split operations in 2:
  - packages (deterministic build)
  - apps (deterministic build + possibly non-deterministic execution)

Basically:
- if your operation depends on inputs that you CANT write on the Nix derivation then it's an app, otherwise it's a package
- An app builds the package under the hood and then runs the binary

Examples:
- Building the terraform binary is deterministic. It's a package, you take
  source code, a compiler, dependencies, and produce a binary. Building it
  always give the same result: a binary
- Executing terraform is not deterministic, it may produce different results each time, requires Internet Network availability,
  depends on remote AWS inputs that you can't state on the Nix derivation. It's an app
- Linting something depends only on the source code.
  Since you can declare the source code as an input in the Nix derivation,
  it's a build
- Unit testing is a build, you can declare code+dependencies in Nix
- Functional testing of a deployed server (selenium) is an app,
  it depends on a remote server that you can't specify on Nix

Remember:
- **Even apps can be deterministically built**,
  there is no pain big enough to drop this decision
- It's just their execution which may vary

So, we want to:
- Build everything deterministically (packages)
- Then execute, if needed (apps)

How is this implemented?
- `makeDerivation` builds deterministically whatever you need
- `makeEntrypoint` builds deterministically whatever you need and
  produce an executable that you can run
- You can declare `makeDerivation`s as inputs to a `makeEntrypoint`,
  helping you compose your monolith out of small `makeDerivation`ed components
