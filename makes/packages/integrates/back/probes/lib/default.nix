{ integratesPkgs
, makeTemplate
, path
, ...
} @ _:
makeTemplate integratesPkgs {
  name = "integrates-back-probes-lib";
  searchPaths = {
    envPaths = [
      integratesPkgs.awscli
      integratesPkgs.curl
      integratesPkgs.gnugrep
    ];
  };
  template = path "/makes/packages/integrates/back/probes/lib/template.sh";
}
