{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  name = "integrates-coverage";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.git
      inputs.nixpkgs.python37Packages.codecov
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/coverage/entrypoint.sh";
}
