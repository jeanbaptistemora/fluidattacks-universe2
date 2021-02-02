path: pkgs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envLsof = "${pkgs.lsof}/bin/lsof";
  };
  location = "";
  name = "makes-utils-kill-pid-listening-on-port";
  template = path "/makes/utils/kill-pid-listening-on-port/entrypoint.sh";
}
