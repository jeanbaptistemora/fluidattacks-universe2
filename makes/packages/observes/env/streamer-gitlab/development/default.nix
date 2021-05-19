{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-streamer-gitlab-development";
  searchPaths = {
    envPaths = [
      streamer-gitlab.development.python
    ];
    envPython38Paths = [
      streamer-gitlab.development.python
    ];
    envSources = [
      streamer-gitlab.runtime
    ];
  };
}
