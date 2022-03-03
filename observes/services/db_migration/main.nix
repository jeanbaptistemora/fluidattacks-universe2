fetchNixpkgs:
let
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };
  system = "x86_64-linux";
  pkg = import ./. {
    inherit legacy_pkgs system;
    src = ./.;
  };
in
pkg
