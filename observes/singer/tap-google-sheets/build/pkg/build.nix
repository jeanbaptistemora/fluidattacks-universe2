{
  lib,
  src,
  metadata,
  runtime_deps,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  version = metadata.version;
  propagatedBuildInputs = runtime_deps;
  # buildInputs = build_deps;
  # checkInputs = test_deps;
  pythonImportsCheck = ["tap_google_sheets"];
  doCheck = false;
  inherit src;
}
