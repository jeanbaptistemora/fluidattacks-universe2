{ makes
, packages
, ...
}:
makes.makeScript {
  name = "forces";
  searchPaths = {
    source = [ packages.forces.config-runtime ];
  };
  entrypoint = ./entrypoint.sh;
}
