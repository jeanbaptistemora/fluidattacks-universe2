{
  nixpkgs,
  projectPath,
  python_version,
  utils-logger,
}: let
  src = projectPath "/observes/common/postgres-client/src";
in
  import src {
    inherit python_version src;
    legacy_pkgs =
      nixpkgs
      // {
        "${python_version}Packages" =
          nixpkgs."${python_version}Packages"
          // {
            utils-logger = utils-logger."${python_version}".pkg;
          };
      };
  }
