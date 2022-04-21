{
  lib,
  src,
  metadata,
  propagatedBuildInputs,
  nativeBuildInputs,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  version = metadata.version;
  format = "pyproject";
  doCheck = true;
  pythonImportsCheck = [pname];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
