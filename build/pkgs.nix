{ commit ? "58ef958f705a028afb01d7a00bf20e6c80d11503"
, digest ? "1cwi7sl9vqjq14qn22vgji2jjax6ppwszwk0ci1xfi63ysflwjrr"
, repo ? "https://github.com/NixOS/nixpkgs"
}:

with import <nixpkgs> { };

let
  nixpkgs = fetchzip {
    sha256 = digest;
    url = "${repo}/archive/${commit}.zip";
  };
in

import nixpkgs { }
