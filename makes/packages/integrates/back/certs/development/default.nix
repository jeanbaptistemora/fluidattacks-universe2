{ makeDerivation
, nixpkgs
, path
, ...
}:
makeDerivation {
  builder = path "/makes/packages/integrates/back/certs/development/builder.sh";
  name = "integrates-back-certs-development";
  searchPaths = {
    envPaths = [ nixpkgs.openssl ];
  };
}
