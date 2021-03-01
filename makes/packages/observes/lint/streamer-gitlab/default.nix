{ path, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.jobs.lint.streamerGitlabDev
