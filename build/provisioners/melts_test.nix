let
  pkgs = import ../pkgs/melts.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.gcc
        pkgs.docker
        pkgs.python37
        pkgs.awscli
        pkgs.sops
      ];

      pyPkgProspector = builders.pythonPackage {
        requirement = "prospector[with_everything]==1.3.0";
      };
      pyPkgPytest = builders.pythonPackage {
        requirement = "pytest==5.1.2";
      };
      pyPkgPytestCov = builders.pythonPackage {
          requirement = "pytest-cov==2.7.1";
      };
      pyPkgPytestXdist = builders.pythonPackage {
          requirement = "pytest-xdist==1.29.0";
      };
      pyPkgPytestRandomOrder = builders.pythonPackage {
          requirement = "pytest-random-order==1.0.4";
      };
      pyPkgPytestRerunfailures = builders.pythonPackage {
          requirement = "pytest-rerunfailures==9.0";
      };
      pyPkgLocalstack = builders.pythonPackage {
          requirement = "localstack==0.11.0.5";
      };

      pyPkgAsserts = import ../../asserts pkgs;

      pyPkgMelts = import ../../melts pkgs;

    })
  )
