{
  observesIndex,
  lib,
  nixpkgs,
  projectPath,
  python_version,
  system,
}: let
  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  typing_ext_override = python_pkgs: pkg_override ["typing-extensions" "typing_extensions"] python_pkgs.typing-extensions;

  override_1 = python_pkgs:
    python_pkgs
    // {
      typing-extensions = import ./typing-extensions {
        inherit lib;
        python_pkgs = nixpkgs."${python_version}Packages";
      };
    };
  override_2 = python_pkgs:
    python_pkgs
    // {
      click = import ./click {
        inherit lib python_pkgs;
      };
    };
  override_3 = python_pkgs:
    python_pkgs
    // {
      import-linter = import ./import-linter {
        inherit lib python_pkgs;
      };
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix lib python_pkgs;
      returns = import ./returns {
        inherit lib python_pkgs;
      };
      types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
      types-click = import ./click/stubs.nix lib;
      types-psycopg2 = import ./psycopg2/stubs.nix lib;
    };
  override_4 = let
    _utils_logger."${python_version}" = import ./utils-logger {
      inherit observesIndex nixpkgs projectPath python_version;
    };
    _legacy_postgres_client."${python_version}" = import ./legacy/postgres-client.nix {
      inherit nixpkgs projectPath python_version;
      utils-logger = _utils_logger;
    };
    _legacy_singer_io."${python_version}" = import ./legacy/singer-io.nix {
      inherit nixpkgs projectPath python_version system;
    };
    _fa_purity = import ./fa-purity {inherit system nixpkgs;};
    _fa_singer_io = import ./fa-singer-io {
      inherit nixpkgs system;
      purity = _fa_purity;
    };
  in
    python_pkgs:
      python_pkgs
      // {
        fa-purity = _fa_purity."${python_version}".pkg;
        fa-singer-io = _fa_singer_io."${python_version}".pkg;
        legacy-postgres-client = _legacy_postgres_client."${python_version}".pkg;
        legacy-singer-io = _legacy_singer_io."${python_version}".pkg;
        utils-logger = _utils_logger."${python_version}".pkg;
      };
  override_5 = python_pkgs: builtins.mapAttrs (_: typing_ext_override python_pkgs) python_pkgs;
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose [override_1 override_2 override_3 override_4 override_5] (nixpkgs."${python_version}Packages");
in
  final_nixpkgs
