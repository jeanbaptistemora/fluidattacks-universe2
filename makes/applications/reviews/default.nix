{ makes
, packages
, ...
}:
makes.makeScript {
  searchPaths = {
    source = [ packages.reviews.runtime ];
  };
  name = "reviews";
  entrypoint = ./entrypoint.sh;
}
