{ path, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.binaries.difGitlabEtl
