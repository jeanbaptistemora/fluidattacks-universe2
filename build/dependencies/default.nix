pkgs:

let
  legacy.kubernetes-helm =
    let
      _pkgs = import ../pkgs/import-src.nix {
        repo = "https://github.com/NixOS/nixpkgs";
        commit = "77cbf0db0ac5dc065969d44aef2cf81776d11228";
        digest = "0lnqqbvb3dv2gmi2dgmqlxlfhb9hvj19llw5jcfd7nc02yqlk1k7";
      };
    in
      _pkgs.kubernetes-helm;

  modules.build.pythonPackage = import ../modules/builders/python-package pkgs;
  modules.env.python = import ../modules/environments/python pkgs;
in rec {
    all = with pkgs; [
      aws-iam-authenticator
      awscli
      bash
      cacert
      coreutils
      curl
      docker
      envsubst
      git
      jq
      kubectl
      legacy.kubernetes-helm
      modules.env.python
      nix
      nix-linter
      nss
      openssl
      python.mandrill
      python.prospector
      shellcheck
      sops
      terraform
      tflint
      which
    ];

    python.mandrill = modules.build.pythonPackage "mandrill-really-maintained==1.2.4";
    python.prospector = modules.build.pythonPackage "prospector[with_everything]==1.2.0";
  }
