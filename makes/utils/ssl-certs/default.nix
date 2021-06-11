path: pkgs:

{ days ? 365
, keyType ? "rsa:4096"
, name
, options
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  nix = import (path "/makes/utils/nix") path pkgs;
in
makeDerivation {
  arguments = {
    envDays = builtins.toString days;
    envKeyType = keyType;
    envOptions = nix.asBashArray options;
  };
  builder = path "/makes/utils/ssl-certs/builder.sh";
  name = "ssl-certs-for-${name}";
  searchPaths = {
    envPaths = [ pkgs.openssl ];
  };
}
