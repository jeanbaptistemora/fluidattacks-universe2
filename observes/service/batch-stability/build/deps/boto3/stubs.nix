lib: python_pkgs: let
  botocore-stubs = lib.buildPythonPackage rec {
    pname = "botocore-stubs";
    version = "1.25.10";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256-PIYSyJF0hD65IwUjxpgdl1GhL6gDiagbydQXwse3irg=";
    };
    propagatedBuildInputs = [python_pkgs.typing-extensions];
  };
  boto3-stubs = lib.buildPythonPackage rec {
    pname = "boto3-stubs";
    version = "1.22.10";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256-P3d9/x6lABlPx5vCGICtb9yuowDsiB4vr/c8rdYlew4=";
    };
    propagatedBuildInputs = [botocore-stubs];
  };
in
  lib.buildPythonPackage rec {
    pname = "types-boto3";
    version = "1.0.2";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256-FfP/rQMU5AoHCP7CX5SJFBT5MmAgJCK/ixm2kThTyYM=";
    };
    propagatedBuildInputs = [boto3-stubs];
  }
