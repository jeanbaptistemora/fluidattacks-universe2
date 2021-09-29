{ inputs
, makeScript
, ...
}:
makeScript {
  name = "integrates-back-authz-matrix";
  replace.__argIntegratesEnv__ = inputs.product.integrates-back-env;
  searchPaths.pythonPackage37 = [ inputs.nixpkgs.python37Packages.pandas ];
  entrypoint = ./entrypoint.sh;
}
