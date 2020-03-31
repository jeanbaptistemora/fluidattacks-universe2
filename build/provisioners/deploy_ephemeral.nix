let
  pkgs = import ../pkgs/stable.nix;
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
        pkgs.awscli
      ];

      pyPkgPelican = builders.pythonPackage "pelican==4.2.0";
      pyPkgWebAssets = builders.pythonPackage "webassets==2.0";
      pyPkgBS4 = builders.pythonPackage "beautifulsoup4==4.8.2";
      pyPkgBabel = builders.pythonPackage "Babel==2.5.3";
      pyPkgcssmin = builders.pythonPackage "cssmin==0.2.0";
    })
  )
