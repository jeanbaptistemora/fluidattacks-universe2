lib: python_pkgs:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-dynamodb";
  version = "1.23.0";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "z9Lg2ISfgIZMXBYX+Utk+RpczFQIihCqgZAQLdtnW88=";
  };
  nativeBuildInputs = with python_pkgs; [boto3];
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}
