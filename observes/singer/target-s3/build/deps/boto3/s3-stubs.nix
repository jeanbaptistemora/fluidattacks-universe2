{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-s3";
  version = "1.23.0";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "0uSc1vOdsUVkEl8fcfXuewcN6+QQIma6R168Az9xyT4=";
  };
  nativeBuildInputs = with python_pkgs; [boto3];
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}
