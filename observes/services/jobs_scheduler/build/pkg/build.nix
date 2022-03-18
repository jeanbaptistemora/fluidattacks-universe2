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
  type_check = ./check/types.sh;
  test_check = ./check/tests.sh;
  installCheckPhase = [
    ''
      source ${type_check} \
      && source ${test_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname "utils_logger.v2"];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
