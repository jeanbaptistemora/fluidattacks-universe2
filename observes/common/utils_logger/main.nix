fetchNixpkgs: let
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };
  pkg = import ./. {
    inherit legacy_pkgs;
    src = ./.;
    python_version = "python39";
  };
in
  pkg
