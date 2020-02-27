import ./fetch-src.nix {
  repo = "https://github.com/NixOS/nixpkgs";
  commit = "ca3531850844e185d483fb878fcd00c6b44069e5";
  digest = "1s1zhzdbmdd7l936g7ydzsjqdi5k5ch6vpjilil0jiwjhrpkw3m4";
}

# This is the nixpkgs set where https://github.com/NixOS/nixpkgs/issues/80086 was solved
#   repo = "https://github.com/NixOS/nixpkgs";
#   commit = "b14afe1ec3fbbb196666bf95e77a1d8235ba0012";
#   digest = "10xm7lslxwqgj8d4jsmwdwr0z1j5zn70014gv890lwc7r6nyv146";
