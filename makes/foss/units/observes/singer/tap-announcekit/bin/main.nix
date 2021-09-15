{ makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argEntrypoint__ = "from tap_announcekit.cli import main";
  };
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-announcekit/env/runtime"
    ];
  };
  name = "observes-tap-announcekit-bin";
  entrypoint = ../../../generic/runner_template.sh;
}
