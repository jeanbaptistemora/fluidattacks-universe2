{
  lib,
  python_pkgs,
}:
python_pkgs.pytz.overridePythonAttrs (
  old: rec {
    version = "2021.1";
    src = lib.fetchPypi {
      inherit version;
      pname = old.pname;
      sha256 = "g6SpCJS/OOJDzwUsi1jzgb/pp6SD9qnKsUC8f3AqxNo=";
    };
  }
)
