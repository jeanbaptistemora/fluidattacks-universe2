import ./fetch-src.nix {
  repo = "https://github.com/NixOS/nixpkgs";
  commit = "b78092a5511bfedb9b344543d30acb176d2b840d";
  digest = "0prv61cf37rpixmc62jln1xdzbw5vqnq944110smkgbhdrgvi512";
}

# This is the nixpkgs set where https://github.com/NixOS/nixpkgs/issues/80086 was solved
#   repo = "https://github.com/NixOS/nixpkgs";
#   commit = "b14afe1ec3fbbb196666bf95e77a1d8235ba0012";
#   digest = "10xm7lslxwqgj8d4jsmwdwr0z1j5zn70014gv890lwc7r6nyv146";
