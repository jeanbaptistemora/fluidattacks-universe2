let
  pkgs = import ../pkgs/stable.nix;

  builders.nodeJsModule = import ../builders/nodejs-module pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.cacert
        pkgs.curl
        pkgs.git
        pkgs.nodejs
        pkgs.python37
      ];

      androidSdk = (pkgs.androidenv.composeAndroidPackages {
        abiVersions = [ "x86" "x86_64" ];
        platformVersions = [ "29" ];
      }).androidsdk;

      JAVA_HOME = pkgs.openjdk;
      ANDROID_SDK_ROOT="${androidSdk}/libexec/android-sdk";

      nodeJsModuleAppium =
        builders.nodeJsModule {
          moduleName = "appium";
          requirement = "appium@1.18.0";
        };

      pyPkgReqsTests =
        builders.pythonRequirements ../../integrates/mobile/e2e/requirements.txt;
    })
  )
