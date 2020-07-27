with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "product";

  repoBuild = ./build;
  repoSkims = ./skims;
  repoReviews = ./reviews;

  src = ./bin;

  installPhase = ''
    mkdir -p "$out"
    mkdir -p "$out/bin"

    install "$src/"* "$out/bin"
    cp -r "$repoBuild" "$out/build"
    cp -r "$repoSkims" "$out/skims"
    cp -r "$repoReviews" "$out/reviews"
  '';
}
