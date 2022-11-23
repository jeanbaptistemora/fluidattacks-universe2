lib:
lib.buildPythonPackage rec {
  pname = "types-python-dateutil";
  version = "2.8.12";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:7zBTt0XwHERDtRK2s9WwT7ry1HaqUDtsyTIEah7fpWo=";
  };
}
