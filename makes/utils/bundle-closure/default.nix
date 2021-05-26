_: nixpkgs:
let
  src = nixpkgs.fetchzip {
    url = "https://github.com/matthewbauer/nix-bundle/archive/8e396533ef8f3e8a769037476824d668409b4a74.tar.gz";
    sha256 = "3HN8pNxH8v+37z9L1Hr6WeyliOEDiN8F2eqAC1ICONM=";
  };
in
import src { inherit nixpkgs; }
