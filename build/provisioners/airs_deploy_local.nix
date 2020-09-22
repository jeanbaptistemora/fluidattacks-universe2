let
  pkgs = import ../pkgs/airs.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.glibcLocales
        pkgs.cacert
        pkgs.asciidoctor
        pkgs.nodejs
        pkgs.python38
        pkgs.rsync
      ];

      pyPkgPelican = builders.pythonPackage {
        requirement = "pelican==4.2.0";
      };
      pyPkgWebAssets = builders.pythonPackage {
        requirement = "webassets==2.0";
      };
      pyPkgBS4 = builders.pythonPackage {
        requirement = "beautifulsoup4==4.8.2";
      };
      pyPkgBabel = builders.pythonPackage {
        requirement = "Babel==2.5.3";
      };
      pyPkgcssmin = builders.pythonPackage {
        requirement = "cssmin==0.2.0";
      };
    })
  )
