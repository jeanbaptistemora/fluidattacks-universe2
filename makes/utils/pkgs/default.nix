{
  commit,
  config ? {},
  digest,
}:

let
  hostPkgs = import <nixpkgs> { };
  pkgsSrc = hostPkgs.fetchzip {
    url = "https://github.com/NixOS/nixpkgs/archive/${commit}.zip";
    sha256 = digest;
  };
in
  import pkgsSrc config
