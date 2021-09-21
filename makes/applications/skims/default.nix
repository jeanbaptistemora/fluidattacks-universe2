{ makes
, packages
, ...
}:
makes.makeScript {
  name = "skims";
  entrypoint = ./entrypoint.sh;
  searchPaths = {
    source = [ packages.skims.config-runtime ];
  };
}
