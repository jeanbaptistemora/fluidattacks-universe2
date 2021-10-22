{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "gitlab")
    ];
  };
  name = "observes-bin-update-project-variable";
  entrypoint = ./entrypoint.sh;
}
