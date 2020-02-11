pkgs:

let
  modules.env.python = import ../../env/python pkgs;
in
  with pkgs; [
    bash
    docker
    git
    hadolint
    nix-linter
    modules.env.python
    shellcheck
    which
  ]
