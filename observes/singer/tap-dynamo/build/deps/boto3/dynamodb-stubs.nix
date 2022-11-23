{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-dynamodb";
  version = "1.24.27";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "yYLST5slJacPQIrUDv9pZg1WkoIXWX2IhgtgQ2sl778=";
  };
  nativeBuildInputs = with python_pkgs; [boto3];
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}
