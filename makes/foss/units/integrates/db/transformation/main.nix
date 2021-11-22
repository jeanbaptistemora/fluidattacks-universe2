{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  env = {
    envDbData = projectPath "/integrates/back/tests/data";
    envNewDbDesign = projectPath "/integrates/arch";
  };
  name = "integrates-db-data-transformation";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.gnused
      inputs.nixpkgs.jq
    ];
  };
  builder = ./builder.sh;
}
