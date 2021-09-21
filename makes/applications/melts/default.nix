{ makes
, packages
, ...
}:
makes.makeScript {
  name = "melts";
  searchPaths = {
    source = [ packages.melts.config-runtime ];
  };
  entrypoint = ./entrypoint.sh;
}
