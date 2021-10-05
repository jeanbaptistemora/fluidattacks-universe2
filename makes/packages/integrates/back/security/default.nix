{ nixpkgs
, makeDerivation
, path
, ...
} @ _:
makeDerivation {
  arguments = {
    envSrcIntegratesBack = path "/integrates/back";
  };
  builder = path "/makes/packages/integrates/back/security/builder.sh";
  name = "integrates-back-security";
  searchPaths = {
    envPaths = [ nixpkgs.python39Packages.bandit ];
  };
}
