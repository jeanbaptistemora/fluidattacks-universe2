{ makes
, nixpkgs
, packages
, ...
}:
makes.makeScript {
  name = "integrates-cache";
  searchPaths = {
    bin = [
      nixpkgs.redis
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  entrypoint = ./entrypoint.sh;
}
