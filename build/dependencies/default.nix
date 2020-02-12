pkgs:

let
  modules.build.pythonPackage = import ../modules/builders/python-package pkgs;
  modules.env.python = import ../modules/environments/python pkgs;
in rec {
    all = with pkgs; [
      awscli
      aws-iam-authenticator
      bash
      cacert
      docker
      git
      jq
      kubectl
      nix-linter
      modules.env.python
      python.prospector
      shellcheck
      terraform
      tflint
      sops
      which
    ];

    python.prospector = modules.build.pythonPackage "prospector[with_everything]==1.2.0";
  }
