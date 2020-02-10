{ repo
, commit
, digest
}:

with import <nixpkgs> { };

let
  nixpkgs = fetchzip {
    url = "${repo}/archive/${commit}.zip";
    sha256 = digest;
  };
in

import nixpkgs { }
