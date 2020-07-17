let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.unzip
        pkgs.python37
      ];

      pyPkgReqsForces =
        builders.pythonRequirements ../../forces/requirements.txt;
      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgForces =
        import ../../forces pkgs;
    })
  )
