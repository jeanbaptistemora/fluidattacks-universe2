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
  self_pycurl = inputs.nixpkgs.python39Packages.pycurl.overridePythonAttrs (_: rec {
    doCheck = false;
    version = "7.45.2";
  });
  self_inotify = inputs.nixpkgs.python39Packages.inotify.overridePythonAttrs (_: rec {
    doCheck = false;
    prePatch = ''
      # Needed while some patches arrive upstream https://github.com/dsoprea/PyInotify/pull/88
      substituteInPlace inotify/adapters.py \
        --replace "_IS_DEBUG = bool(int(os.environ.get('DEBUG', '0')))" "_IS_DEBUG = False"
    '';
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
        self_inotify
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
        "${self_inotify}/lib/python3.9/site-packages/"
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
