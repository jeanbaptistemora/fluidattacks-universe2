let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ [
          pkgs.git
          pkgs.glibcLocales
          pkgs.sops
          pkgs.awscli
          pkgs.python38
          pkgs.jq
          pkgs.curl
          pkgs.cacert
        ];

        pyPkgMandrill = builders.pythonPackage "mandrill-37==1.1.0";
        pyPkgGitPython = builders.pythonPackage "GitPython==3.1.0";
    })
  )
