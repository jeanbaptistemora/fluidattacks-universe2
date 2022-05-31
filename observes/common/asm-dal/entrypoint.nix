fetchNixpkgs: let
  system = "x86_64-linux";
  python_version = "python310";
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _fa_purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.18.1";
  };
  fa-purity = import _fa_purity_src {
    inherit system legacy_pkgs;
    src = _fa_purity_src;
  };

  local_pkgs = {inherit fa-purity;};
  out = import ./. {
    inherit python_version;
    pkgs = legacy_pkgs // local_pkgs;
    src = ./.;
  };
in
  out
