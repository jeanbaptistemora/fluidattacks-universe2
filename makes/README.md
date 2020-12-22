# Architectural Decision Record

# 2020-12-20 - Why rewriting the whole build system

- Writing a pure build system is painful for 1 developer, 1 time
- Using a pure build system is delicious for all developers, all times thereafter
- See: https://gitlab.com/fluidattacks/product/-/issues/3836, for details

# 2020-12-21 - Why ./make instead of `nix flake`

- Procedures can be executed at 1 command of distance, easy to remember
- Teaching ./make to people is teaching:
  - How to install nix
  - How to type ./make in the console
- Teaching flakes to people in non-NixOS systems is teaching:
  - How to install nix
  - How to set the nix.conf with needed configuration values
  - How to use the new CLI
  - How to use nix-shell with a long -I nixpkgs=hash
  - How to build/run apps and packages from the flake
- ./make uses flakes under the hood, but hides/automatize the complexity
