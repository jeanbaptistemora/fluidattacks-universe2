{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  env = {
    envAirs = projectPath "/airs";
    envExclude = ./exclude.lst;
  };
  builder = ./builder.sh;
  name = "airs-lint-content";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
    ];
    source = [
      inputs.product.airs-adoc-linter
    ];
  };
}
