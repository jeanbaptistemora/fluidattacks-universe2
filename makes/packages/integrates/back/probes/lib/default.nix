{ integratesPkgs
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path integratesPkgs;
in
makeTemplate {
  arguments = {
    envAws = "${integratesPkgs.awscli}/bin/aws";
    envCurl = "${integratesPkgs.curl}/bin/curl";
    envGrep = "${integratesPkgs.gnugrep}/bin/grep";
  };
  name = "integrates-back-probes-lib";
  template = path "/makes/packages/integrates/back/probes/lib/template.sh";
}
