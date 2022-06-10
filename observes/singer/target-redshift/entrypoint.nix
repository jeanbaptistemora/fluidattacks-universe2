fetchNixpkgs: projectPath: observesIndex: let
  system = "x86_64-linux";
  python_version = "python310";
  legacy_pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit legacy_pkgs python_version;
    src = _utils_logger_src;
  };

  local_pkgs = {inherit utils-logger;};
  out = import ./. {
    inherit python_version system;
    nixpkgs = legacy_pkgs // local_pkgs;
    src = ./.;
  };
in
  out
