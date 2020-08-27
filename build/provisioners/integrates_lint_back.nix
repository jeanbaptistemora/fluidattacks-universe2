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
        pkgs.nodejs
      ];

      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/containers/app/requirements.txt;
      pyPkgReqs =
        builders.pythonRequirements ../../integrates/deploy/dependencies/dev-requirements.txt;

      pyPkgIntegratesBack =
        import ../../integrates/django-apps/integrates-back-async pkgs;
    })
  )
