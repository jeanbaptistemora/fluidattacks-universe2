{
  lib,
  nixpkgs,
  python_version,
  system,
}: let
  pkg_override = names: (import ./pkg_override.nix) (x: builtins.elem x.pname names);
  _python_pkgs = nixpkgs."${python_version}Packages";
  fa-purity = import ./fa-purity {inherit nixpkgs system;};
  python_pkgs =
    _python_pkgs
    // {
      click = import ./click {
        inherit lib;
        python_pkgs = _python_pkgs;
      };
      fa-purity = fa-purity."${python_version}".pkg;
      fa-singer-io =
        (import ./fa-singer-io {
          inherit nixpkgs system;
          purity = fa-purity;
        })
        ."${python_version}"
        .pkg;
      import-linter = import ./import-linter {
        inherit lib;
        python_pkgs = _python_pkgs;
      };
    };
  typing_ext_override = pkg_override ["typing-extensions" "typing_extensions"] python_pkgs.typing-extensions;
  click_override = pkg_override ["click"] python_pkgs.click;
in
  python_pkgs
  // {
    import-linter = click_override python_pkgs.import-linter;
    mypy = typing_ext_override python_pkgs.mypy;
    returns = import ./returns {
      inherit lib python_pkgs;
    };
  }
