with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "product";

  repoAsserts = ./asserts;
  repoBuild = ./build;
  repoObserves = ./observes;
  repoReviews = ./reviews;

  src = ./bin;

  installPhase = ''
    mkdir -p "$out"
    mkdir -p "$out/bin"

    install "$src/"* "$out/bin"
    cp -r "$repoAsserts" "$out/asserts"
    cp -r "$repoBuild" "$out/build"
    cp -r "$repoObserves" "$out/observes"
    cp -r "$repoReviews" "$out/reviews"
  '';
}
