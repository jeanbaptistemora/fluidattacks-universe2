{
  lib,
  pkgs,
  python_version,
}: let
  pkg_override = import ./pkg_override.nix;
  _python_pkgs = pkgs."${python_version}Packages";
  python_pkgs =
    _python_pkgs
    // {
      click = import ./click {
        inherit lib;
        python_pkgs = _python_pkgs;
      };
      fa-purity = pkgs.fa-purity."${python_version}".pkg;
      import-linter = import ./import-linter {
        inherit lib;
        python_pkgs = _python_pkgs;
      };
    };
  typing_ext_override = pkg_override (x: (x.pname == "typing-extensions" || x.pname == "typing_extensions")) python_pkgs.typing-extensions;
  click_override = pkg_override (x: (x.pname == "click")) python_pkgs.click;
in
  python_pkgs
  // {
    import-linter = click_override python_pkgs.import-linter;
    mypy = typing_ext_override python_pkgs.mypy;
    returns = import ./returns {
      inherit lib python_pkgs;
    };
  }
