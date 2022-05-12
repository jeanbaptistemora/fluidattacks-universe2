lib: python_pkgs:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-batch";
  version = "1.22.8";
  src = lib.fetchPypi {
    inherit pname version;
    hash = "sha256-Wfnmws8tf1FoNFwRLlsDO/mhMZsJM/hMq6jfxjlTP50=";
  };
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}
