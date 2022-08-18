{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };

  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;

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
      pytestCheckHook = python_pkgs.pytestCheckHook.override {
        pytest = typing_ext_override python_pkgs python_pkgs.pytest;
      };
      pytz = import ./pytz lib python_pkgs;
      jsonschema = import ./jsonschema lib python_pkgs;
    };
  override_3 = python_pkgs:
    python_pkgs
    // {
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix lib python_pkgs;
      types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
      types-click = import ./click/stubs.nix lib;
      types-psycopg2 = import ./psycopg2/stubs.nix lib;
    };
  override_4 = python_pkgs:
    python_pkgs
    // {
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
      redshift-client = nixpkgs.redshift-client."${python_version}".pkg;
    };
  typing_ext_override = python_pkgs: pkg_override ["typing-extensions" "typing_extensions"] python_pkgs.typing-extensions;
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  jsonschema_override = python_pkgs: pkg_override ["jsonschema"] python_pkgs.jsonschema;
  fa_purity_override = python_pkgs: pkg_override ["fa_purity"] python_pkgs.fa-purity;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    typing_ext_override
    pycheck_override
    pytz_override
    jsonschema_override
    fa_purity_override
  ];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose ([override_1 override_2 override_3 override_4] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
