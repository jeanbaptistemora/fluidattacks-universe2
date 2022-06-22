{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "typing_extensions";
  format = "pyproject";
  version = "4.2.0";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "8cJGVaDaDRtn8H4XpeayoQWJTmgkuSCWN4uzZo7wI3Y=";
  };
  nativeBuildInputs = [python_pkgs.flit-core];
}
