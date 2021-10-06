{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-back-authz-matrix";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
  searchPaths.pythonPackage39 = [ inputs.nixpkgs.python39Packages.pandas ];
  entrypoint = ./entrypoint.sh;
}
