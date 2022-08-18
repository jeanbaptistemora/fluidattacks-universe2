{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "import-linter";
  version = "1.2.6";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:0fjUy8CnuzAwt3ONfi6tz/kY8HCp2wUiuV3yqINNR94=";
  };
  propagatedBuildInputs = with python_pkgs; [grimp click];
}
