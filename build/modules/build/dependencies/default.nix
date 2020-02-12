pkgs:

let
  modules.build.pythonPackage = import ../python-package pkgs;
  modules.env.python = import ../../env/python pkgs;
in rec {
    all = with pkgs; [
      bash
      docker
      git
      nix-linter
      modules.env.python
      python.prospector
      shellcheck
      which
    ];

    python.prospector = modules.build.pythonPackage "prospector[with_everything]==1.2.0";
  }
