{ makes
, packages
, importUtility
, nixpkgs
, ...
}:
makes.makeScript {
  replace = {
    __argGetConfig__ = ./src/get_config.py;
  };
  name = "skims-process-group";
  searchPaths = {
    bin = [
      packages.melts
      packages.skims
      nixpkgs.jq
      nixpkgs.yq
    ];
    source = [
      packages.skims.config-runtime
      (importUtility "aws")
      (importUtility "env")
      (importUtility "git")
      (importUtility "sops")
      (importUtility "time")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
