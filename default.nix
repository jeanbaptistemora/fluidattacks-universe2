with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "product";

  repoAsserts = ./asserts;
  repoBuild = ./build;
  repoMelts = ./melts;
  repoSkims = ./skims;
  repoReviews = ./reviews;

  src = ./bin;

  installPhase = ''
    mkdir -p "$out"
    mkdir -p "$out/bin"

    install "$src/"* "$out/bin"
    cp -r "$repoAsserts" "$out/asserts"
    cp -r "$repoBuild" "$out/build"
    cp -r "$repoMelts" "$out/melts"
    cp -r "$repoSkims" "$out/skims"
    cp -r "$repoReviews" "$out/reviews"
  '';
}
