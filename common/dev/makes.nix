{
  __nixpkgs__,
  outputs,
  ...
}: {
  dev = {
    common = {
      bin = [
        __nixpkgs__.alejandra
        outputs."/common/dev/fmt"
      ];
    };
  };
}
