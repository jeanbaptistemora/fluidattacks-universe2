{ importUtility
, makes
, packages
, ...
}:
makes.makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      (importUtility "aws")
      (importUtility "sops")
      packages.sorts.config-runtime
    ];
  };
  entrypoint = ./entrypoint.sh;
}
