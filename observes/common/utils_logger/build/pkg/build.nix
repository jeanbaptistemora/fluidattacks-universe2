{ lib
, src
, propagatedBuildInputs
, nativeBuildInputs
}:
lib.buildPythonPackage rec {
  pname = "utils_logger";
  version = "1.0.0";
  format = "pyproject";
  doCheck = false;
  pythonImportsCheck = [ "utils_logger" ];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
