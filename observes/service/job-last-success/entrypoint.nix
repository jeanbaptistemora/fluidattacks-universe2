fetchNixpkgs: projectPath: observesIndex: let
  python_version = "python310";
  pkgs = fetchNixpkgs {
    rev = "6c5e6e24f0b3a797ae4984469f42f2a01ec8d0cd";
    sha256 = "0ayz07vsl38h9jsnib4mff0yh3d5ajin6xi3bb2xjqwmad99n8p6";
  };

  _utils_logger_src = projectPath observesIndex.common.utils_logger.root;
  utils-logger."${python_version}" = import _utils_logger_src {
    inherit python_version;
    src = _utils_logger_src;
    legacy_pkgs = pkgs;
  };

  local_pkgs = {inherit utils-logger;};
  out = import ./. {
    inherit local_pkgs pkgs python_version;
    src = ./.;
  };
in
  out
