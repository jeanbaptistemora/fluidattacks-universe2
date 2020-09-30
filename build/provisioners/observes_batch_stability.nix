let
  pkgs = import ../pkgs/observes.nix;

  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.git
        pkgs.python3
        (builders.pythonPackage {}).propagatedBuildInputs
      ];

      pyPkgBoto3 = builders.pythonPackage {
        requirement ="boto3==1.15.9";
      };

      pyPkgBugsnag = builders.pythonPackage {
        requirement ="bugsnag==3.6.1";
      };
    })
  )
