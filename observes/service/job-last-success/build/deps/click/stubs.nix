lib:
lib.buildPythonPackage rec {
  pname = "types-click";
  version = "7.1.8";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:tmBJaL5kAdxRYxHKUHCKCii6p6DLhA79dBLw27/04JI=";
  };
}
