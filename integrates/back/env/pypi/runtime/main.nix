{
  makeTemplate,
  makePythonPypiEnvironment,
  outputs,
  projectPath,
  inputs,
  ...
}: let
  self_bugsnag = inputs.nixpkgs.python39Packages.bugsnag.overridePythonAttrs (_: rec {
    src =
      builtins.fetchGit
      {
        url = "https://github.com/fluidattacks/bugsnag-python";
        ref = "master";
        rev = "41387bcff4ae94ae633725889cb55567bcce5c9e";
      };
    doCheck = false;
  });
  # 3.11 compatible but version release is still pending
  self_h2 = inputs.nixpkgs.python39Packages.h2.overridePythonAttrs (old: rec {
    src = inputs.nixpkgs.fetchFromGitHub {
      owner = "python-hyper";
      repo = old.pname;
      rev = "bc005afad8302549facf5afde389a16759b2ccdb";
      hash = "sha256-Q+bw8SjLQGPl7zX7NpM25723moV6N5lQ6VNIpNNCTdI=";
    };
  });
  # https://github.com/montag451/pypi-mirror/issues/21
  self_hypercorn = inputs.nixpkgs.python39Packages.hypercorn.overridePythonAttrs (old: rec {
    doCheck = false;
    propagatedBuildInputs = [
      inputs.nixpkgs.python39Packages.priority
      inputs.nixpkgs.python39Packages.toml
      inputs.nixpkgs.python39Packages.wsproto
      self_h2
    ];
    src = inputs.nixpkgs.fetchFromGitHub {
      owner = "pgjones";
      repo = old.pname;
      rev = version;
      hash = "sha256-ECREs8UwqTWUweUrwnUwpVotCII2v4Bz7ZCk3DSAd8I=";
    };
    version = "0.14.3";
  });
  # Needed by celery to work with sqs.
  # Couldn't install via yaml due to missing curl-config binary
  # Currently outdated in the pinned nixpkgs revision
  self_pycurl = inputs.nixpkgs.python39Packages.pycurl.overridePythonAttrs (_: rec {
    version = "7.45.2";
  });
  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-back-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsBuild = {
      bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
    };
    searchPathsRuntime = {
      bin = [
        inputs.nixpkgs.gcc
        inputs.nixpkgs.postgresql
        inputs.nixpkgs.gnutar
        inputs.nixpkgs.gzip
        self_hypercorn
        self_pycurl
      ];
    };
    withSetuptools_57_4_0 = true;
    withWheel_0_37_0 = true;
  };
in
  makeTemplate {
    name = "integrates-back-pypi-runtime";
    searchPaths = {
      pythonPackage = [
        "${self_bugsnag}/lib/python3.9/site-packages/"
        "${self_hypercorn}/lib/python3.9/site-packages/"
        "${self_pycurl}/lib/python3.9/site-packages/"
        (projectPath "/integrates/back/src")
        (projectPath "/integrates")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        pythonRequirements
        outputs."/common/utils/safe-pickle"
        outputs."/common/utils/serializers"
        outputs."/common/utils/git_self"
      ];
    };
  }
