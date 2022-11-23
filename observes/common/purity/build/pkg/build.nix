{
  lib,
  src,
  metadata,
  build_deps,
  runtime_deps,
  test_deps,
}:
lib.buildPythonPackage rec {
  inherit src;
  pname = metadata.name;
  version = metadata.version;
  format = "pyproject";
  doCheck = true;
  pythonImportsCheck = [pname];
  buildInputs = build_deps;
  propagatedBuildInputs = runtime_deps;
  checkInputs = test_deps;
}
