{ makesPkgs
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path makesPkgs;
in
makeTemplate {
  arguments = {
    envBase64 = "${makesPkgs.coreutils}/bin/base64";
    envChmod = "${makesPkgs.coreutils}/bin/chmod";
    envSshKeyGen = "${makesPkgs.openssh}/bin/ssh-keygen";
  };
  name = "makes-cache-config";
  template = path "/makes/packages/makes/cache/config/template.sh";
}
