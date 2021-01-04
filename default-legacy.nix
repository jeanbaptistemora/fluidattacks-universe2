with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "product";

  repoAsserts = ./asserts;
  repoBuild = ./build;
  repoForces = ./forces;
  repoMelts = ./melts;
  repoObserves = ./observes;
  repoSkims = ./skims;
  repoSorts = ./sorts;
  repoReviews = ./reviews;

  src = ./bin;

  installPhase = ''
    mkdir -p "$out"
    mkdir -p "$out/bin"

    install "$src/"* "$out/bin"
    cp -r "$repoAsserts" "$out/asserts"
    cp -r "$repoBuild" "$out/build"
    cp -r "$repoForces" "$out/forces"
    cp -r "$repoMelts" "$out/melts"
    cp -r "$repoObserves" "$out/observes"
    cp -r "$repoSkims" "$out/skims"
    cp -r "$repoSorts" "$out/sorts"
    cp -r "$repoReviews" "$out/reviews"
  '';
}
