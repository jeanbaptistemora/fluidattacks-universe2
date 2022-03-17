{
  lib,
  pythonPkgs,
}:
lib.buildPythonPackage rec {
  pname = "returns";
  version = "0.19.0";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256:RUS7Z4ScHvG794I3WdQzp3OVnlt3qP0G0B/vbQYPKsU=";
  };
  doCheck = false;
  propagatedBuildInputs = [pythonPkgs.typing-extensions];
}
