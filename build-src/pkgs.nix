with import <nixpkgs> { };

let
  repo = "https://github.com/NixOS/nixpkgs";
  commit = "58ef958f705a028afb01d7a00bf20e6c80d11503";
  digest = "1cwi7sl9vqjq14qn22vgji2jjax6ppwszwk0ci1xfi63ysflwjrr";

  pkgs = fetchzip {
    url = "${repo}/archive/${commit}.zip";
    sha256 = digest;
  };
in

import pkgs { }
