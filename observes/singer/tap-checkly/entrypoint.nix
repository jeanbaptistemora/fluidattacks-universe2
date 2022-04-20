fetchNixpkgs: projectPath: observesIndex: let
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };
  local_lib = {
    utils-logger = projectPath observesIndex.common.utils_logger.root;
    paginator = projectPath "/observes/common/paginator";
    legacy_purity = projectPath "/observes/common/purity";
    singer_io = projectPath "/observes/common/singer_io";
  };
  out = import ./. {
    system = "x86_64-linux";
    inherit legacy_pkgs local_lib;
    src = ./.;
  };
in
  out
