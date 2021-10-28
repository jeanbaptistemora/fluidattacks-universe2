{ makeScript
, inputs
, ...
}:
makeScript {
  name = "makes-done";
  searchPaths = {
    bin = [
      inputs.nixpkgs.netcat
      inputs.product.makes-kill-port
    ];
  };
  entrypoint = ./entrypoint.sh;
}
