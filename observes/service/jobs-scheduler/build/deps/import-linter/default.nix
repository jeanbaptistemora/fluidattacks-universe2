{
  lib,
  click,
  networkx,
}: let
  grimp = lib.buildPythonPackage rec {
    pname = "grimp";
    version = "1.2.3";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256:v+4uMpCESktuAI9nwH2rVPOHA/wL8BYRGaVHMbob7Q0=";
    };
    doCheck = false;
    propagatedBuildInputs = [networkx];
  };
in
  lib.buildPythonPackage rec {
    pname = "import-linter";
    version = "1.2.6";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256:0fjUy8CnuzAwt3ONfi6tz/kY8HCp2wUiuV3yqINNR94=";
    };
    propagatedBuildInputs = [grimp click];
  }
