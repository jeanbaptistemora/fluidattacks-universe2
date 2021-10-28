{ __nixpkgs__
, inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "airs-fontawesome";
  searchPaths = {
    bin = [
      inputs.nixpkgs.autoconf
      inputs.nixpkgs.bash
      inputs.nixpkgs.binutils.bintools
      inputs.nixpkgs.gcc
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.gnumake
      inputs.nixpkgs.gnused
      inputs.nixpkgs.nodejs
      inputs.nixpkgs.python37
    ];
    source = [
      (makeTemplate {
        name = "vips";
        searchPaths = {
          export = [
            [ "CPATH" inputs.nixpkgs.glib.dev "/include/glib-2.0" ]
            [ "CPATH" inputs.nixpkgs.glib.out "/lib/glib-2.0/include" ]
            [ "CPATH" __nixpkgs__.vips.dev "/include" ]
          ];
        };
      })
    ];
  };
  template = ./template.sh;
}
