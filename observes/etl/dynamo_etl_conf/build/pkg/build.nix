{
  lib,
  src,
  propagatedBuildInputs,
  nativeBuildInputs,
}:
lib.buildPythonPackage rec {
  pname = "dynamo_etl_conf";
  version = "0.1.0";
  format = "pyproject";
  checkInputs = [
    lib.pytestCheckHook
  ];
  doCheck = true;
  pythonImportsCheck = ["dynamo_etl_conf"];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
