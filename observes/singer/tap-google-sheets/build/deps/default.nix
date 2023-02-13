{
  nixpkgs,
  python_version,
}: let
  utils = import ./override_utils.nix;
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
    inherit (nixpkgs) fetchFromGitHub;
  };
  python_pkgs = nixpkgs."${python_version}Packages";

  backoff = python_pkgs.backoff.overridePythonAttrs (
    old: rec {
      version = "1.8.0";
      src = lib.fetchFromGitHub {
        owner = "litl";
        repo = old.pname;
        rev = "refs/tags/v${version}";
        sha256 = "XI1LL7k3+G2yeMIKuXo4rhfapUd3gI6BfnpgQvWzl1U=";
      };
    }
  );
  urllib3 = python_pkgs.urllib3.overridePythonAttrs (
    old: rec {
      version = "1.25.11";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "jX6qWoKhysIyFkmQ8Eh0xZTJRT7FXu8C6riFqgL8F6I=";
      };
    }
  );

  idna = python_pkgs.idna.overridePythonAttrs (
    old: rec {
      version = "2.8";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "w1ez9ijPU64sTAVifsxIRVMULKIyZOWT0ye83l6cNAc=";
      };
    }
  );

  requests = python_pkgs.requests.overridePythonAttrs (
    old: rec {
      version = "2.22.0";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "EeAHqKKqAyP1qSHp5qLX5OZ9mHfoV3P7qbpkGQJcvrQ=";
      };
      doCheck = false;
    }
  );

  jsonschema = python_pkgs.jsonschema.overridePythonAttrs (
    old: rec {
      version = "2.6.0";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "b/XzGAhwg2yuQPBvoQQZ9VcggXXxOte8Jsqne+sfbgI=";
      };
      propagatedBuildInputs = old.propagatedBuildInputs ++ (with python_pkgs; [vcversioner]);
      doCheck = false;
    }
  );

  simplejson = python_pkgs.simplejson.overridePythonAttrs (
    old: rec {
      version = "3.11.1";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "AaItSd3ZoWixNvJsrIfZozVmDOB6pcYwuONgfW9DJec=";
      };
    }
  );

  chardet = python_pkgs.chardet.overridePythonAttrs (
    old: rec {
      version = "3.0.4";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "hKuS7RxNTxaRbgWQa2t1psD7XbghzGXnDL1ko+Kl6q4=";
      };
      doCheck = false;
    }
  );

  jeepney = python_pkgs.jeepney.overridePythonAttrs (
    _: rec {
      buildInputs = with python_pkgs; [outcome trio];
    }
  );

  singer-python = python_pkgs.buildPythonPackage rec {
    pname = "singer-python";
    version = "5.12.2";
    propagatedBuildInputs = with python_pkgs; [
      backoff
      ciso8601
      jsonschema
      pytz
      python-dateutil
      simplejson
    ];
    src = lib.fetchPypi {
      inherit pname version;
      sha256 = "xciOZEz1t1oEdGLtE8hoalvoIluHfbhxiX/pUqMXAD8=";
    };
    doCheck = false;
  };

  chardet_override = utils.replace_pkg ["chardet"] chardet;
  urllib3_override = utils.replace_pkg ["urllib3"] urllib3;
  idna_override = utils.replace_pkg ["idna"] idna;
  jeepney_override = utils.replace_pkg ["jeepney"] jeepney;

  full_override = utils.compose [
    idna_override
    chardet_override
    urllib3_override
    jeepney_override
    utils.no_check_override
  ];
in {
  inherit lib;
  python_pkgs =
    python_pkgs
    // {
      backoff = full_override backoff;
      requests = full_override requests;
      singer-python = full_override singer-python;
    };
}
