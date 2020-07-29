let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        pkgs.curl
        pkgs.cacert
        pkgs.python37
      ];

      pyPkgGitPython = builders.pythonPackage {
        requirement = "GitPython==3.1.0";
      };
    })
  )
