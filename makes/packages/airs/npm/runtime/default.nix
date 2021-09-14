{ nixpkgs
, makes
, makeTemplate
, path
, ...
}:
makeTemplate {
  name = "airs-fontawesome";
  searchPaths = {
    envPaths = [
      nixpkgs.autoconf
      nixpkgs.bash
      nixpkgs.binutils.bintools
      nixpkgs.gcc
      nixpkgs.gnugrep
      nixpkgs.gnumake
      nixpkgs.gnused
      nixpkgs.nodejs
      nixpkgs.python37
    ];
    envSources = [
      (makes.makeTemplate {
        replace.__argGlibDev__ = nixpkgs.glib.dev;
        replace.__argGlibOut__ = nixpkgs.glib.out;
        replace.__argVips__ = makes.__nixpkgs__.vips.dev;
        name = "vips";
        template = ''
          export CPATH=/not-set
          export CPATH=__argGlibDev__/include/glib-2.0:$CPATH
          export CPATH=__argGlibOut__/lib/glib-2.0/include:$CPATH
          export CPATH=__argVips__/include:$CPATH
        '';
      })
    ];
  };
  template = path "/makes/packages/airs/npm/runtime/template.sh";
}
