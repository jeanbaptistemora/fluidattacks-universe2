{
  lib,
  src,
  metadata,
  build_deps,
  runtime_deps,
  test_deps,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  version = metadata.version;
  format = "pyproject";
  type_check = ./check/types.sh;
  test_check = ./check/tests.sh;
  arch_check = ./check/arch.sh;
  checkPhase = [
    ''
      source ${type_check} \
      && source ${test_check} \
      && source ${arch_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname];
  buildInputs = build_deps;
  propagatedBuildInputs = runtime_deps;
  checkInputs = test_deps;
  inherit src;
}
