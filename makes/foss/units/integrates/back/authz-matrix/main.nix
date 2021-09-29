{ inputs
, makeScript
, ...
}:
makeScript {
  name = "integrates-back-authz-matrix";
  replace.__argIntegratesEnv__ = inputs.product.integrates-back-env;
  searchPaths.pythonPackage39 = [ inputs.nixpkgs.python39Packages.pandas ];
  entrypoint = ./entrypoint.sh;
}
